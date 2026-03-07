"""
FastDC Message Scheduler — Send messages after a delay
"""

import asyncio
import logging
from typing import Optional

import discord
from discord.ext import commands

logger = logging.getLogger('fastdc.scheduler')


class MessageScheduler:
    """
    Handles scheduling messages to be sent after a delay.
    
    Usage:
        scheduler = MessageScheduler(bot)
        scheduler.schedule(channel_id=123, message="Hello!", delay_seconds=60)
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.tasks = []

    def schedule(self, channel_id: int, message: str, delay_seconds: float) -> asyncio.Task:
        """
        Schedule a message to be sent after a delay.
        
        Parameters:
        ----------
        channel_id : int
            The ID of the channel to send the message to
        message : str
            The message content
        delay_seconds : float
            Delay in seconds before sending
        """
        task = self.bot.loop.create_task(self._delayed_send(channel_id, message, delay_seconds))
        self.tasks.append(task)
        logger.info(f"Scheduled message to channel {channel_id} in {delay_seconds}s")
        return task

    async def _delayed_send(self, channel_id: int, message: str, delay: float):
        """Internal method to wait and then send"""
        await asyncio.sleep(delay)
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
            logger.info(f"Sent scheduled message to #{channel.name}")
        else:
            logger.warning(f"Channel {channel_id} not found for scheduled message")

    def cancel_all(self):
        """Cancel all pending scheduled messages"""
        for task in self.tasks:
            if not task.done():
                task.cancel()
        self.tasks.clear()
        logger.info("All scheduled messages cancelled")
