"""
FastDC Event Logging — Track commands, errors, and bot events
"""

import logging
from discord.ext import commands

logger = logging.getLogger('fastdc.events')


def setup_event_logging(bot_instance):
    """Register event logging handlers"""
    bot = bot_instance.bot

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Please wait **{error.retry_after:.1f}s** before using this command again.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 You don't have permission to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"⚠️ Missing argument: `{error.param.name}`")
        elif isinstance(error, commands.CommandNotFound):
            pass  # Silently ignore unknown commands
        else:
            logger.error(f"Command error in {ctx.command}: {str(error)}")

    @bot.event
    async def on_command(ctx):
        logger.info(f"Command: {ctx.command.name} | User: {ctx.author} | Server: {ctx.guild}")
