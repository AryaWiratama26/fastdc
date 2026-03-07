"""
FastDC Utility Commands — ping, serverinfo, bothelp (prefix + slash)
"""

import discord
from discord import app_commands
from discord.ext import commands

from ..utils.embed_builder import QuickEmbed


def setup_utility_commands(bot_instance):
    """Register utility commands (prefix and slash)"""
    bot = bot_instance.bot

    # --- Prefix Commands ---

    @bot.command()
    async def ping(ctx):
        latency = round(bot.latency * 1000)
        embed = QuickEmbed.build(
            title="🏓 Pong!",
            description=f"Latency: **{latency}ms**",
            color=QuickEmbed.SUCCESS if latency < 200 else QuickEmbed.WARNING
        )
        await ctx.send(embed=embed)

    @bot.command()
    async def serverinfo(ctx):
        guild = ctx.guild
        embed = QuickEmbed.build(
            title=f"📊 {guild.name} Info",
            color=QuickEmbed.PRIMARY,
            fields=[
                ("Server ID", str(guild.id), True),
                ("Created On", guild.created_at.strftime("%Y-%m-%d"), True),
                ("Member Count", str(guild.member_count), True),
                ("Channel Count", str(len(guild.channels)), True),
                ("Role Count", str(len(guild.roles)), True),
                ("Boost Level", str(guild.premium_tier), True),
            ],
            thumbnail=guild.icon.url if guild.icon else None
        )
        await ctx.send(embed=embed)

    # --- Slash Commands ---

    @bot.tree.command(name='ping', description='Check bot latency')
    async def ping_slash(interaction: discord.Interaction):
        latency = round(bot.latency * 1000)
        embed = QuickEmbed.build(
            title="🏓 Pong!",
            description=f"Latency: **{latency}ms**",
            color=QuickEmbed.SUCCESS if latency < 200 else QuickEmbed.WARNING
        )
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='serverinfo', description='Display server information')
    async def serverinfo_slash(interaction: discord.Interaction):
        guild = interaction.guild
        embed = QuickEmbed.build(
            title=f"📊 {guild.name} Info",
            color=QuickEmbed.PRIMARY,
            fields=[
                ("Server ID", str(guild.id), True),
                ("Created On", guild.created_at.strftime("%Y-%m-%d"), True),
                ("Member Count", str(guild.member_count), True),
                ("Channel Count", str(len(guild.channels)), True),
                ("Role Count", str(len(guild.roles)), True),
                ("Boost Level", str(guild.premium_tier), True),
            ],
            thumbnail=guild.icon.url if guild.icon else None
        )
        await interaction.response.send_message(embed=embed)


def setup_help(bot_instance):
    """Register the bothelp command"""
    bot = bot_instance.bot

    @bot.group(invoke_without_command=True)
    async def bothelp(ctx):
        embed = QuickEmbed.build(
            title="📖 FastDC Bot Help",
            description="Use `!bothelp <command>` for more info on a command",
            color=QuickEmbed.INFO,
            fields=[
                ("🤖 AI Commands", "`!ai` `/ai`", False),
                ("🛡️ Moderation", "`!kick` `!ban` `!clear`\n`/kick` `/ban` `/clear`", False),
                ("🔧 Utility", "`!ping` `!serverinfo`\n`/ping` `/serverinfo`", False),
                ("📊 Fun", "`!poll`  `/poll`", False),
                ("🎫 Support", "`!ticket` `!close`\n`/ticket` `/close`", False),
            ],
            footer="FastDC Bot Framework"
        )
        await ctx.send(embed=embed)

    @bot.tree.command(name='help', description='Show all available commands')
    async def help_slash(interaction: discord.Interaction):
        embed = QuickEmbed.build(
            title="📖 FastDC Bot Help",
            description="Here are all available commands:",
            color=QuickEmbed.INFO,
            fields=[
                ("🤖 AI Commands", "`/ai`", False),
                ("🛡️ Moderation", "`/kick` `/ban` `/clear`", False),
                ("🔧 Utility", "`/ping` `/serverinfo`", False),
                ("📊 Fun", "`/poll`", False),
                ("🎫 Support", "`/ticket` `/close`", False),
            ],
            footer="FastDC Bot Framework"
        )
        await interaction.response.send_message(embed=embed)
