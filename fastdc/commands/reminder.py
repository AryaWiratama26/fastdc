"""
FastDC Reminder — Set reminders that DM you after a delay
"""

import asyncio
import re
import logging

import discord
from discord import app_commands
from discord.ext import commands

from ..utils.embed_builder import QuickEmbed

logger = logging.getLogger('fastdc.reminder')


def parse_duration(duration_str: str) -> int:
    """Parse duration string like '30s', '5m', '1h' to seconds"""
    match = re.match(r'^(\d+)([smhd])$', duration_str.lower())
    if not match:
        return 0
    amount = int(match.group(1))
    unit = match.group(2)
    multipliers = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    return amount * multipliers.get(unit, 0)


def format_duration(seconds: int) -> str:
    if seconds >= 86400:
        return f"{seconds // 86400} day(s)"
    elif seconds >= 3600:
        return f"{seconds // 3600} hour(s)"
    elif seconds >= 60:
        return f"{seconds // 60} minute(s)"
    return f"{seconds} second(s)"


def setup_reminder_commands(bot_instance):
    """Register reminder commands"""
    bot = bot_instance.bot

    async def _send_reminder(user, message, channel, delay):
        await asyncio.sleep(delay)
        embed = QuickEmbed.build(
            title="⏰ Reminder!",
            description=message,
            color=QuickEmbed.WARNING,
            timestamp=True
        )
        try:
            await user.send(embed=embed)
        except discord.Forbidden:
            # Can't DM, send in channel instead
            await channel.send(f"{user.mention}", embed=embed)

    @bot.command()
    async def remind(ctx, duration: str, *, message: str):
        seconds = parse_duration(duration)
        if seconds <= 0:
            await ctx.send(embed=QuickEmbed.warning(
                "Invalid Duration",
                "Use format: `30s`, `5m`, `1h`, `2d`\nExample: `!remind 30m Check the oven`"
            ))
            return

        embed = QuickEmbed.success(
            "Reminder Set",
            f"I'll remind you in **{format_duration(seconds)}**: {message}"
        )
        await ctx.send(embed=embed)
        bot.loop.create_task(_send_reminder(ctx.author, message, ctx.channel, seconds))
        logger.info(f"Reminder set by {ctx.author.name} for {format_duration(seconds)}")

    @bot.tree.command(name='remind', description='Set a reminder')
    @app_commands.describe(duration='When to remind (e.g. 30s, 5m, 1h)', message='What to remind you about')
    async def remind_slash(interaction: discord.Interaction, duration: str, message: str):
        seconds = parse_duration(duration)
        if seconds <= 0:
            await interaction.response.send_message(embed=QuickEmbed.warning(
                "Invalid Duration",
                "Use format: `30s`, `5m`, `1h`, `2d`"
            ), ephemeral=True)
            return

        embed = QuickEmbed.success(
            "Reminder Set",
            f"I'll remind you in **{format_duration(seconds)}**: {message}"
        )
        await interaction.response.send_message(embed=embed)
        bot.loop.create_task(_send_reminder(interaction.user, message, interaction.channel, seconds))
