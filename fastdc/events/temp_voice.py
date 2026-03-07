"""
FastDC Temp Voice Channels — Auto-create/delete voice channels
"""

import logging
import discord

logger = logging.getLogger('fastdc.temp_voice')


def setup_temp_voice(bot_instance, trigger_channel_id: int, category_id: int = None):
    """
    Register temp voice channel handlers.

    Parameters:
    ----------
    trigger_channel_id : int
        ID of the "Join to Create" voice channel
    category_id : int, optional
        Category to create temp channels in (defaults to trigger channel's category)
    """
    bot = bot_instance.bot
    temp_channels = set()  # Track created channel IDs

    @bot.event
    async def on_voice_state_update(member, before, after):
        # User joined the trigger channel → create temp VC
        if after.channel and after.channel.id == trigger_channel_id:
            guild = member.guild

            category = None
            if category_id:
                category = guild.get_channel(category_id)
            elif after.channel.category:
                category = after.channel.category

            new_channel = await guild.create_voice_channel(
                name=f"🔊 {member.display_name}'s Channel",
                category=category,
                overwrites={
                    member: discord.PermissionOverwrite(
                        manage_channels=True,
                        move_members=True
                    )
                }
            )
            temp_channels.add(new_channel.id)
            await member.move_to(new_channel)
            logger.info(f"Created temp VC '{new_channel.name}' for {member.name}")

        # User left a temp channel → delete if empty
        if before.channel and before.channel.id in temp_channels:
            if len(before.channel.members) == 0:
                temp_channels.discard(before.channel.id)
                await before.channel.delete()
                logger.info(f"Deleted empty temp VC '{before.channel.name}'")
