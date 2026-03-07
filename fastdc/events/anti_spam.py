"""
FastDC Anti-Spam — Detect and handle spam messages automatically.
Also integrates: auto-reply, AFK system, leveling XP, custom commands.
"""

import logging
import random
from collections import defaultdict
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from ..models import AntiSpamConfig
from ..utils.embed_builder import QuickEmbed

logger = logging.getLogger('fastdc.anti_spam')


def setup_anti_spam(bot_instance, config: AntiSpamConfig = None):
    """
    Register the unified on_message handler.
    Handles: anti-spam, auto-reply, AFK, leveling XP, custom commands.
    """
    if config is None:
        config = bot_instance.anti_spam_config

    bot = bot_instance.bot
    message_tracker = defaultdict(list)

    @bot.event
    async def on_message(message):
        if message.author.bot or not message.guild:
            await bot.process_commands(message)
            return

        user_id = message.author.id
        content_lower = message.content.lower()

        for rule in bot_instance.auto_replies:
            if rule.trigger in content_lower:
                await message.channel.send(rule.response)
                break

        if hasattr(bot_instance, '_afk_users'):
            afk_users = bot_instance._afk_users

            # Remove AFK if user sends a message
            if user_id in afk_users:
                reason = afk_users.pop(user_id)
                embed = QuickEmbed.info("Welcome Back", f"{message.author.mention} is no longer AFK.")
                await message.channel.send(embed=embed, delete_after=5)

            # Notify if mentioned user is AFK
            for mentioned in message.mentions:
                if mentioned.id in afk_users:
                    reason = afk_users[mentioned.id]
                    embed = QuickEmbed.info(
                        "User is AFK",
                        f"**{mentioned.display_name}** is AFK: {reason}"
                    )
                    await message.channel.send(embed=embed, delete_after=5)

        if hasattr(bot_instance, '_xp_data') and hasattr(bot_instance, '_xp_per_message'):
            from ..commands.leveling import level_from_xp
            xp_data = bot_instance._xp_data
            guild_id = message.guild.id
            old_xp = xp_data[guild_id][user_id]
            xp_gain = random.randint(10, bot_instance._xp_per_message + 10)
            xp_data[guild_id][user_id] += xp_gain

            old_level = level_from_xp(old_xp)
            new_level = level_from_xp(xp_data[guild_id][user_id])

            if new_level > old_level:
                embed = QuickEmbed.build(
                    title="🎉 Level Up!",
                    description=f"{message.author.mention} reached **Level {new_level}**!",
                    color=discord.Color.gold()
                )
                await message.channel.send(embed=embed, delete_after=10)

        if hasattr(bot_instance, '_custom_commands'):
            prefix = bot.command_prefix
            if content_lower.startswith(prefix):
                cmd_name = content_lower[len(prefix):].split()[0]
                if cmd_name in bot_instance._custom_commands:
                    await message.channel.send(bot_instance._custom_commands[cmd_name])

        now = datetime.now()
        cutoff = now - timedelta(seconds=config.interval_seconds)
        message_tracker[user_id] = [t for t in message_tracker[user_id] if t > cutoff]
        message_tracker[user_id].append(now)

        if len(message_tracker[user_id]) > config.max_messages:
            member = message.author
            logger.warning(f"Spam detected from {member.name}")

            if config.action == "mute":
                try:
                    await member.timeout(
                        timedelta(seconds=config.mute_duration),
                        reason="Anti-spam: Too many messages"
                    )
                    embed = QuickEmbed.warning("Anti-Spam", f"{member.mention} has been muted for {config.mute_duration}s")
                    await message.channel.send(embed=embed)
                except discord.Forbidden:
                    logger.error(f"Cannot mute {member.name}")

            elif config.action == "kick":
                try:
                    await member.kick(reason="Anti-spam: Too many messages")
                    embed = QuickEmbed.warning("Anti-Spam", f"**{member.name}** has been kicked (spam)")
                    await message.channel.send(embed=embed)
                except discord.Forbidden:
                    logger.error(f"Cannot kick {member.name}")

            elif config.action == "warn":
                embed = QuickEmbed.warning("Spam Warning", f"{member.mention}, slow down! You're sending messages too fast.")
                await message.channel.send(embed=embed)

            message_tracker[user_id] = []

        await bot.process_commands(message)
