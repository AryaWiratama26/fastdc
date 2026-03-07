"""
FastDC Starboard — Repost popular messages to a starboard channel
"""

import logging
import discord

from ..utils.embed_builder import QuickEmbed

logger = logging.getLogger('fastdc.starboard')


def setup_starboard(bot_instance, channel_id: int, emoji: str = "⭐", threshold: int = 3):
    """
    Register starboard event handlers.

    Parameters:
    ----------
    channel_id : int
        ID of the starboard channel
    emoji : str
        The emoji to track (default: ⭐)
    threshold : int
        Minimum reactions needed to post to starboard (default: 3)
    """
    bot = bot_instance.bot
    posted_messages = set()  

    @bot.event
    async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
        if str(payload.emoji) != emoji:
            return

        channel = bot.get_channel(payload.channel_id)
        if not channel:
            return

        message = await channel.fetch_message(payload.message_id)

        # Don't starboard messages from the starboard channel
        if message.channel.id == channel_id:
            return

        # Count matching reactions
        reaction_count = 0
        for reaction in message.reactions:
            if str(reaction.emoji) == emoji:
                reaction_count = reaction.count
                break

        if reaction_count >= threshold and message.id not in posted_messages:
            posted_messages.add(message.id)

            starboard_channel = bot.get_channel(channel_id)
            if not starboard_channel:
                logger.error(f"Starboard channel {channel_id} not found")
                return

            embed = discord.Embed(
                description=message.content or "*[No text content]*",
                color=discord.Color.gold(),
                timestamp=message.created_at
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.avatar.url if message.author.avatar else None
            )
            embed.add_field(name="Source", value=f"[Jump to message]({message.jump_url})", inline=False)
            embed.set_footer(text=f"{emoji} {reaction_count}")

            # Attach first image if any
            if message.attachments:
                embed.set_image(url=message.attachments[0].url)

            await starboard_channel.send(embed=embed)
            logger.info(f"Message {message.id} posted to starboard ({reaction_count} {emoji})")
