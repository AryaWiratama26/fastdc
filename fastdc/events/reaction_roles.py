"""
FastDC Reaction Roles — React to a message to get a role
"""

import logging
import discord

from ..models import ReactionRoleMapping

logger = logging.getLogger('fastdc.reaction_roles')


def setup_reaction_roles(bot_instance):
    """
    Register reaction role event handlers.
    Reads mappings from bot_instance.reaction_roles list.
    """
    bot = bot_instance.bot

    @bot.event
    async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
        if payload.user_id == bot.user.id:
            return

        for mapping in bot_instance.reaction_roles:
            if payload.message_id == mapping.message_id and str(payload.emoji) == mapping.emoji:
                guild = bot.get_guild(payload.guild_id)
                if guild:
                    role = guild.get_role(mapping.role_id)
                    member = guild.get_member(payload.user_id)
                    if role and member:
                        await member.add_roles(role)
                        logger.info(f"Added role '{role.name}' to {member.name}")
                break

    @bot.event
    async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
        if payload.user_id == bot.user.id:
            return

        for mapping in bot_instance.reaction_roles:
            if payload.message_id == mapping.message_id and str(payload.emoji) == mapping.emoji:
                guild = bot.get_guild(payload.guild_id)
                if guild:
                    role = guild.get_role(mapping.role_id)
                    member = guild.get_member(payload.user_id)
                    if role and member:
                        await member.remove_roles(role)
                        logger.info(f"Removed role '{role.name}' from {member.name}")
                break
