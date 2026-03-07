"""
FastDC Leveling/XP System — Track user activity, level up, leaderboard
"""

import math
import logging
from collections import defaultdict

import discord
from discord import app_commands
from discord.ext import commands

from ..utils.embed_builder import QuickEmbed

logger = logging.getLogger('fastdc.leveling')

# XP formula: level = floor(sqrt(xp / 100))
# Reverse calculation: xp needed for level = level^2 * 100


def xp_for_level(level: int) -> int:
    """Calculate total XP needed for a given level"""
    return level * level * 100


def level_from_xp(xp: int) -> int:
    """Calculate level from total XP"""
    return int(math.sqrt(xp / 100))


def setup_leveling_system(bot_instance):
    """Register leveling/XP system"""
    bot = bot_instance.bot

    xp_data = defaultdict(lambda: defaultdict(int))
    bot_instance._xp_data = xp_data

    def _get_rank_data(guild_id, user_id):
        xp = xp_data[guild_id][user_id]
        level = level_from_xp(xp)
        current_level_xp = xp_for_level(level)
        next_level_xp = xp_for_level(level + 1)
        progress_xp = xp - current_level_xp
        needed_xp = next_level_xp - current_level_xp
        return level, xp, progress_xp, needed_xp

    def _make_progress_bar(progress, total, length=10):
        filled = int((progress / total) * length) if total > 0 else 0
        bar = "█" * filled + "░" * (length - filled)
        return bar

    bot_instance._xp_per_message = 15

    @bot.command()
    async def rank(ctx, member: discord.Member = None):
        member = member or ctx.author
        level, xp, progress, needed = _get_rank_data(ctx.guild.id, member.id)
        bar = _make_progress_bar(progress, needed)

        guild_xp = xp_data[ctx.guild.id]
        sorted_users = sorted(guild_xp.items(), key=lambda x: x[1], reverse=True)
        position = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == member.id), 0)

        embed = QuickEmbed.build(
            title=f"📊 {member.display_name}'s Rank",
            color=QuickEmbed.PRIMARY,
            fields=[
                ("Level", str(level), True),
                ("XP", f"{xp:,}", True),
                ("Rank", f"#{position}", True),
                ("Progress", f"{bar} ({progress}/{needed} XP)", False),
            ],
            thumbnail=member.avatar.url if member.avatar else None
        )
        await ctx.send(embed=embed)

    @bot.command(aliases=['lb', 'top'])
    async def leaderboard(ctx):
        guild_xp = xp_data[ctx.guild.id]
        if not guild_xp:
            await ctx.send(embed=QuickEmbed.info("Leaderboard", "No activity recorded yet."))
            return

        sorted_users = sorted(guild_xp.items(), key=lambda x: x[1], reverse=True)[:10]

        description = ""
        medals = ["🥇", "🥈", "🥉"]
        for i, (user_id, xp) in enumerate(sorted_users):
            member = ctx.guild.get_member(user_id)
            name = member.display_name if member else f"User {user_id}"
            level = level_from_xp(xp)
            medal = medals[i] if i < 3 else f"**{i + 1}.**"
            description += f"{medal} {name} — Level **{level}** ({xp:,} XP)\n"

        embed = QuickEmbed.build(
            title=f"🏆 {ctx.guild.name} Leaderboard",
            description=description,
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @bot.tree.command(name='rank', description='Check your or someone else\'s rank')
    @app_commands.describe(member='The member to check (default: you)')
    async def rank_slash(interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        level, xp, progress, needed = _get_rank_data(interaction.guild.id, member.id)
        bar = _make_progress_bar(progress, needed)

        guild_xp = xp_data[interaction.guild.id]
        sorted_users = sorted(guild_xp.items(), key=lambda x: x[1], reverse=True)
        position = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == member.id), 0)

        embed = QuickEmbed.build(
            title=f"📊 {member.display_name}'s Rank",
            color=QuickEmbed.PRIMARY,
            fields=[
                ("Level", str(level), True),
                ("XP", f"{xp:,}", True),
                ("Rank", f"#{position}", True),
                ("Progress", f"{bar} ({progress}/{needed} XP)", False),
            ],
            thumbnail=member.avatar.url if member.avatar else None
        )
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='leaderboard', description='Show server XP leaderboard')
    async def leaderboard_slash(interaction: discord.Interaction):
        guild_xp = xp_data[interaction.guild.id]
        if not guild_xp:
            await interaction.response.send_message(embed=QuickEmbed.info("Leaderboard", "No activity recorded yet."))
            return

        sorted_users = sorted(guild_xp.items(), key=lambda x: x[1], reverse=True)[:10]

        description = ""
        medals = ["🥇", "🥈", "🥉"]
        for i, (user_id, xp) in enumerate(sorted_users):
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else f"User {user_id}"
            level = level_from_xp(xp)
            medal = medals[i] if i < 3 else f"**{i + 1}.**"
            description += f"{medal} {name} — Level **{level}** ({xp:,} XP)\n"

        embed = QuickEmbed.build(
            title=f"🏆 {interaction.guild.name} Leaderboard",
            description=description,
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)
