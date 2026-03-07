"""
FastDC Ticket System — Create and manage support tickets
"""

import discord
from discord import app_commands
from discord.ext import commands

from ..utils.embed_builder import QuickEmbed


def setup_ticket_commands(bot_instance):
    """Register ticket system commands (prefix and slash)"""
    bot = bot_instance.bot

    async def _create_ticket(guild: discord.Guild, user: discord.Member):
        """Create a private ticket channel"""
        # Find or create Tickets category
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category(
                "Tickets",
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
            )

        # Check for existing ticket
        existing = discord.utils.get(category.text_channels, name=f"ticket-{user.name.lower()}")
        if existing:
            return None, existing

        # Create the ticket channel
        channel = await category.create_text_channel(
            f"ticket-{user.name.lower()}",
            overwrites={
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
        )

        embed = QuickEmbed.build(
            title="🎫 Support Ticket",
            description=(
                f"Hello {user.mention}! Welcome to your support ticket.\n\n"
                f"Please describe your issue and a staff member will assist you.\n"
                f"Use `!close` or `/close` to close this ticket."
            ),
            color=QuickEmbed.INFO,
            footer=f"Ticket created by {user.display_name}",
            timestamp=True
        )
        await channel.send(embed=embed)

        return channel, None

    async def _close_ticket(channel: discord.TextChannel, user: discord.Member):
        """Close a ticket channel"""
        if not channel.name.startswith("ticket-"):
            return False

        embed = QuickEmbed.build(
            title="🎫 Ticket Closed",
            description=f"This ticket was closed by {user.mention}.\nChannel will be deleted in 5 seconds.",
            color=QuickEmbed.ERROR,
            timestamp=True
        )
        await channel.send(embed=embed)

        import asyncio
        await asyncio.sleep(5)
        await channel.delete()
        return True

    # --- Prefix Commands ---

    @bot.command()
    async def ticket(ctx):
        channel, existing = await _create_ticket(ctx.guild, ctx.author)
        if existing:
            await ctx.send(embed=QuickEmbed.warning(
                "Ticket Exists",
                f"You already have an open ticket: {existing.mention}"
            ))
        elif channel:
            await ctx.send(embed=QuickEmbed.success(
                "Ticket Created",
                f"Your ticket has been created: {channel.mention}"
            ))

    @bot.command()
    async def close(ctx):
        closed = await _close_ticket(ctx.channel, ctx.author)
        if not closed:
            await ctx.send(embed=QuickEmbed.warning(
                "Not a Ticket",
                "This command can only be used inside a ticket channel."
            ))

    # --- Slash Commands ---

    @bot.tree.command(name='ticket', description='Create a support ticket')
    async def ticket_slash(interaction: discord.Interaction):
        channel, existing = await _create_ticket(interaction.guild, interaction.user)
        if existing:
            await interaction.response.send_message(embed=QuickEmbed.warning(
                "Ticket Exists",
                f"You already have an open ticket: {existing.mention}"
            ), ephemeral=True)
        elif channel:
            await interaction.response.send_message(embed=QuickEmbed.success(
                "Ticket Created",
                f"Your ticket has been created: {channel.mention}"
            ), ephemeral=True)

    @bot.tree.command(name='close', description='Close the current ticket')
    async def close_slash(interaction: discord.Interaction):
        if not interaction.channel.name.startswith("ticket-"):
            await interaction.response.send_message(embed=QuickEmbed.warning(
                "Not a Ticket",
                "This command can only be used inside a ticket channel."
            ), ephemeral=True)
            return

        await interaction.response.send_message(embed=QuickEmbed.build(
            title="🎫 Closing Ticket...",
            description="This ticket will be deleted in 5 seconds.",
            color=QuickEmbed.ERROR
        ))

        import asyncio
        await asyncio.sleep(5)
        await interaction.channel.delete()
