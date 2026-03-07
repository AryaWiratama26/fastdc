"""
FastDC Giveaway System — Timed giveaways with random winner selection
"""

import asyncio
import random
import re
import logging

import discord
from discord import app_commands
from discord.ext import commands

from ..utils.embed_builder import QuickEmbed

logger = logging.getLogger('fastdc.giveaway')


def parse_duration(duration_str: str) -> int:
    """Parse duration string like '30s', '5m', '1h', '2d' to seconds"""
    match = re.match(r'^(\d+)([smhd])$', duration_str.lower())
    if not match:
        return 0

    amount = int(match.group(1))
    unit = match.group(2)

    multipliers = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    return amount * multipliers.get(unit, 0)


def format_duration(seconds: int) -> str:
    """Format seconds to human readable string"""
    if seconds >= 86400:
        return f"{seconds // 86400} day(s)"
    elif seconds >= 3600:
        return f"{seconds // 3600} hour(s)"
    elif seconds >= 60:
        return f"{seconds // 60} minute(s)"
    return f"{seconds} second(s)"


def setup_giveaway_commands(bot_instance):
    """Register giveaway commands"""
    bot = bot_instance.bot

    async def _run_giveaway(channel, message_obj, duration, prize):
        """Background task to end giveaway after duration"""
        await asyncio.sleep(duration)

        # Re-fetch message to get updated reactions
        try:
            msg = await channel.fetch_message(message_obj.id)
        except discord.NotFound:
            return

        # Get users who reacted with 🎉
        users = []
        for reaction in msg.reactions:
            if str(reaction.emoji) == "🎉":
                async for user in reaction.users():
                    if not user.bot:
                        users.append(user)
                break

        if users:
            winner = random.choice(users)
            embed = QuickEmbed.build(
                title="🎉 Giveaway Ended!",
                description=f"**Prize:** {prize}\n**Winner:** {winner.mention}\n\nCongratulations! 🥳",
                color=discord.Color.gold(),
                timestamp=True
            )
        else:
            embed = QuickEmbed.build(
                title="🎉 Giveaway Ended!",
                description=f"**Prize:** {prize}\n**Winner:** No one entered 😢",
                color=discord.Color.dark_grey(),
                timestamp=True
            )

        await msg.edit(embed=embed)
        if users:
            await channel.send(f"🎉 Congratulations {winner.mention}! You won **{prize}**!")

    # Prefix command: !giveaway 1h Nitro
    @bot.command()
    @commands.has_permissions(manage_guild=True)
    async def giveaway(ctx, duration: str, *, prize: str):
        seconds = parse_duration(duration)
        if seconds <= 0:
            await ctx.send(embed=QuickEmbed.warning(
                "Invalid Duration",
                "Use format: `30s`, `5m`, `1h`, `2d`"
            ))
            return

        embed = QuickEmbed.build(
            title="🎉 GIVEAWAY! 🎉",
            description=f"**Prize:** {prize}\n**Duration:** {format_duration(seconds)}\n**Hosted by:** {ctx.author.mention}\n\nReact with 🎉 to enter!",
            color=discord.Color.gold(),
            footer="Ends soon!",
            timestamp=True
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎉")
        bot.loop.create_task(_run_giveaway(ctx.channel, msg, seconds, prize))

    # Slash command: /giveaway
    @bot.tree.command(name='giveaway', description='Start a giveaway')
    @app_commands.describe(duration='Duration (e.g. 30s, 5m, 1h, 2d)', prize='What to give away')
    @app_commands.checks.has_permissions(manage_guild=True)
    async def giveaway_slash(interaction: discord.Interaction, duration: str, prize: str):
        seconds = parse_duration(duration)
        if seconds <= 0:
            await interaction.response.send_message(embed=QuickEmbed.warning(
                "Invalid Duration",
                "Use format: `30s`, `5m`, `1h`, `2d`"
            ), ephemeral=True)
            return

        embed = QuickEmbed.build(
            title="🎉 GIVEAWAY! 🎉",
            description=f"**Prize:** {prize}\n**Duration:** {format_duration(seconds)}\n**Hosted by:** {interaction.user.mention}\n\nReact with 🎉 to enter!",
            color=discord.Color.gold(),
            footer="Ends soon!",
            timestamp=True
        )
        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response()
        await msg.add_reaction("🎉")
        bot.loop.create_task(_run_giveaway(interaction.channel, msg, seconds, prize))
