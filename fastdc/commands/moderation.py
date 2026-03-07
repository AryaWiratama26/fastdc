"""
FastDC Moderation Commands — kick, ban, clear (prefix + slash)
"""

import discord
from discord import app_commands
from discord.ext import commands

from ..utils.embed_builder import QuickEmbed


def setup_moderation_commands(bot_instance):
    """Register moderation commands (prefix and slash)"""
    bot = bot_instance.bot

    # --- Prefix Commands ---

    @bot.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = QuickEmbed.success("Member Kicked", f"**{member.name}** has been kicked.\nReason: {reason or 'No reason provided'}")
        await ctx.send(embed=embed)

    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = QuickEmbed.success("Member Banned", f"**{member.name}** has been banned.\nReason: {reason or 'No reason provided'}")
        await ctx.send(embed=embed)

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        embed = QuickEmbed.success("Messages Cleared", f"Cleared **{amount}** messages.")
        await ctx.send(embed=embed, delete_after=5)

    # --- Slash Commands ---

    @bot.tree.command(name='kick', description='Kick a member from the server')
    @app_commands.describe(member='The member to kick', reason='Reason for kicking')
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_slash(interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.kick(reason=reason)
        embed = QuickEmbed.success("Member Kicked", f"**{member.name}** has been kicked.\nReason: {reason or 'No reason provided'}")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='ban', description='Ban a member from the server')
    @app_commands.describe(member='The member to ban', reason='Reason for banning')
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_slash(interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.ban(reason=reason)
        embed = QuickEmbed.success("Member Banned", f"**{member.name}** has been banned.\nReason: {reason or 'No reason provided'}")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='clear', description='Clear messages in the channel')
    @app_commands.describe(amount='Number of messages to delete')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear_slash(interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=amount)
        embed = QuickEmbed.success("Messages Cleared", f"Cleared **{amount}** messages.")
        await interaction.followup.send(embed=embed, ephemeral=True)
