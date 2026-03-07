"""
FastDC Welcome & Leave Events — Member join/leave notifications
"""

import discord
from ..utils.helpers import find_channel


def setup_welcome(bot_instance, message: str = "Hello {member}, welcome to Server!"):
    """
    Register welcome message handler.
    
    Parameters:
    ----------
    message : str
        Welcome message template. Use {member} as placeholder.
    """
    bot = bot_instance.bot

    @bot.event
    async def on_member_join(member):
        channel = find_channel(member.guild)

        if "{member}" not in message:
            msg = "Hello {member}, welcome to Server!"
        else:
            msg = message

        if channel:
            await channel.send(msg.replace("{member}", member.mention))


def setup_leave(bot_instance, message: str = "{member} has left the server"):
    """
    Register leave message handler.
    
    Parameters:
    ----------
    message : str
        Leave message template. Use {member} as placeholder.
    """
    bot = bot_instance.bot

    @bot.event
    async def on_member_remove(member):
        channel = find_channel(member.guild)

        if "{member}" not in message:
            msg = "{member} has left the server"
        else:
            msg = message

        if channel:
            await channel.send(msg.replace("{member}", member.name))
