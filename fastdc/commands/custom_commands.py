"""
FastDC Custom Commands — Let admins create/delete commands at runtime
"""

import logging

import discord
from discord import app_commands
from discord.ext import commands

from ..utils.embed_builder import QuickEmbed

logger = logging.getLogger('fastdc.custom_commands')


def setup_custom_commands(bot_instance):
    """Register custom command management"""
    bot = bot_instance.bot
    custom_cmds = {}

    bot_instance._custom_commands = custom_cmds

    @bot.command(name='addcmd')
    @commands.has_permissions(manage_guild=True)
    async def addcmd(ctx, name: str, *, response: str):
        """Add a custom command. Usage: !addcmd hello Hello everyone!"""
        name = name.lower()
        if name in [cmd.name for cmd in bot.commands]:
            await ctx.send(embed=QuickEmbed.warning(
                "Name Conflict",
                f"A built-in command `!{name}` already exists."
            ))
            return

        custom_cmds[name] = response
        if hasattr(bot_instance, 'save_state'):
            bot_instance.save_state()
        embed = QuickEmbed.success(
            "Command Added",
            f"Custom command `!{name}` created!\nResponse: {response}"
        )
        await ctx.send(embed=embed)
        logger.info(f"Custom command '!{name}' added by {ctx.author.name}")

    @bot.command(name='delcmd')
    @commands.has_permissions(manage_guild=True)
    async def delcmd(ctx, name: str):
        """Delete a custom command. Usage: !delcmd hello"""
        name = name.lower()
        if name in custom_cmds:
            del custom_cmds[name]
            if hasattr(bot_instance, 'save_state'):
                bot_instance.save_state()
            await ctx.send(embed=QuickEmbed.success("Command Deleted", f"Custom command `!{name}` removed."))
        else:
            await ctx.send(embed=QuickEmbed.warning("Not Found", f"Custom command `!{name}` doesn't exist."))

    @bot.command(name='listcmds')
    async def listcmds(ctx):
        """List all custom commands"""
        if not custom_cmds:
            await ctx.send(embed=QuickEmbed.info("Custom Commands", "No custom commands yet."))
            return

        cmd_list = "\n".join([f"`!{name}` → {response[:50]}..." if len(response) > 50 else f"`!{name}` → {response}" for name, response in custom_cmds.items()])
        embed = QuickEmbed.build(
            title="📝 Custom Commands",
            description=cmd_list,
            color=QuickEmbed.INFO
        )
        await ctx.send(embed=embed)

    # Slash variants
    @bot.tree.command(name='addcmd', description='Add a custom command')
    @app_commands.describe(name='Command name', response='Response message')
    @app_commands.checks.has_permissions(manage_guild=True)
    async def addcmd_slash(interaction: discord.Interaction, name: str, response: str):
        name = name.lower()
        if name in [cmd.name for cmd in bot.commands]:
            await interaction.response.send_message(embed=QuickEmbed.warning(
                "Name Conflict", f"A built-in command `!{name}` already exists."
            ), ephemeral=True)
            return
        custom_cmds[name] = response
        if hasattr(bot_instance, 'save_state'):
            bot_instance.save_state()
        await interaction.response.send_message(embed=QuickEmbed.success(
            "Command Added", f"Custom command `!{name}` created!\nResponse: {response}"
        ))

    @bot.tree.command(name='delcmd', description='Delete a custom command')
    @app_commands.describe(name='Command name to delete')
    @app_commands.checks.has_permissions(manage_guild=True)
    async def delcmd_slash(interaction: discord.Interaction, name: str):
        name = name.lower()
        if name in custom_cmds:
            del custom_cmds[name]
            if hasattr(bot_instance, 'save_state'):
                bot_instance.save_state()
            await interaction.response.send_message(embed=QuickEmbed.success("Command Deleted", f"`!{name}` removed."))
        else:
            await interaction.response.send_message(embed=QuickEmbed.warning("Not Found", f"`!{name}` doesn't exist."), ephemeral=True)
