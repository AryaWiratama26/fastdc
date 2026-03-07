"""
FastDC Auto Role — Automatically assign a role when members join
"""

import logging
import discord

logger = logging.getLogger('fastdc.auto_role')


def setup_auto_role(bot_instance, role_id: int):
    """
    Register auto-role on member join.

    Parameters:
    ----------
    role_id : int
        The ID of the role to automatically assign
    """
    bot = bot_instance.bot

    @bot.event
    async def on_member_join(member):
        role = member.guild.get_role(role_id)
        if role:
            try:
                await member.add_roles(role)
                logger.info(f"Auto-assigned role '{role.name}' to {member.name}")
            except discord.Forbidden:
                logger.error(f"Cannot assign role '{role.name}' to {member.name}: insufficient permissions")
