"""
FastDC Auto Reply — Supports multiple trigger/response pairs
"""

import logging

logger = logging.getLogger('fastdc.auto_reply')


def setup_auto_reply(bot_instance):
    """
    Register the auto-reply on_message handler.
    Reads triggers from bot_instance.auto_replies list.
    Should be called once after all auto_reply() calls.
    """
    bot = bot_instance.bot

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        content_lower = message.content.lower()
        for rule in bot_instance.auto_replies:
            if rule.trigger in content_lower:
                await message.channel.send(rule.response)
                break  # Only respond to the first matching trigger

        await bot.process_commands(message)
