"""
FastDC AFK System — Set AFK status and notify on mention
"""

import logging
import discord
from discord import app_commands
from discord.ext import commands

from ..utils.embed_builder import QuickEmbed

logger = logging.getLogger('fastdc.afk')


def setup_afk_system(bot_instance):
    """Register AFK commands and mention handler"""
    bot = bot_instance.bot
    afk_users = {}  # {user_id: reason}

    @bot.command()
    async def afk(ctx, *, reason: str = "AFK"):
        afk_users[ctx.author.id] = reason
        embed = QuickEmbed.info("AFK Set", f"{ctx.author.mention} is now AFK: **{reason}**")
        await ctx.send(embed=embed)

    @bot.tree.command(name='afk', description='Set your AFK status')
    @app_commands.describe(reason='Reason for being AFK')
    async def afk_slash(interaction: discord.Interaction, reason: str = "AFK"):
        afk_users[interaction.user.id] = reason
        embed = QuickEmbed.info("AFK Set", f"{interaction.user.mention} is now AFK: **{reason}**")
        await interaction.response.send_message(embed=embed)

    # Store reference so on_message can access it
    bot_instance._afk_users = afk_users
