"""
Unit tests for FastDC MessageScheduler
"""

import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from fastdc.utils.scheduler import MessageScheduler


@pytest.fixture
def mock_bot():
    """Create a mock bot with a loop attribute."""
    bot = MagicMock()
    loop = MagicMock()
    bot.loop = loop
    return bot


@pytest.fixture
def scheduler(mock_bot):
    """Create a MessageScheduler instance with a mock bot."""
    return MessageScheduler(mock_bot)


class TestMessageSchedulerInit:
    """Tests for MessageScheduler initialization."""

    def test_initialization(self, mock_bot):
        """Should store bot reference and start with empty tasks list."""
        s = MessageScheduler(mock_bot)
        assert s.bot is mock_bot
        assert s.tasks == []


class TestMessageSchedulerSchedule:
    """Tests for the schedule() method."""

    def test_schedule_creates_task(self, scheduler, mock_bot):
        """Should create an asyncio task and add it to the tasks list."""
        mock_task = MagicMock()
        mock_bot.loop.create_task.return_value = mock_task

        result = scheduler.schedule(123, "Hello", 60)

        mock_bot.loop.create_task.assert_called_once()
        assert result is mock_task
        assert mock_task in scheduler.tasks

    def test_schedule_multiple(self, scheduler, mock_bot):
        """Should accumulate multiple tasks in the list."""
        mock_bot.loop.create_task.return_value = MagicMock()

        scheduler.schedule(1, "msg1", 10)
        scheduler.schedule(2, "msg2", 20)
        scheduler.schedule(3, "msg3", 30)

        assert len(scheduler.tasks) == 3


class TestMessageSchedulerCancelAll:
    """Tests for the cancel_all() method."""

    def test_cancel_all(self, scheduler):
        """Should cancel running tasks and skip already-done tasks."""
        t1 = MagicMock()
        t1.done.return_value = False
        t2 = MagicMock()
        t2.done.return_value = False
        t3 = MagicMock()
        t3.done.return_value = True

        scheduler.tasks = [t1, t2, t3]
        scheduler.cancel_all()

        t1.cancel.assert_called_once()
        t2.cancel.assert_called_once()
        t3.cancel.assert_not_called()
        assert scheduler.tasks == []

    def test_cancel_all_empty(self, scheduler):
        """Should not raise when called with no tasks."""
        scheduler.cancel_all()
        assert scheduler.tasks == []


class TestMessageSchedulerDelayedSend:
    """Tests for the _delayed_send() coroutine."""

    @pytest.mark.asyncio
    async def test_delayed_send_channel_found(self, scheduler, mock_bot):
        """Should send the message when channel is found."""
        mock_channel = MagicMock()
        mock_channel.send = AsyncMock()
        mock_channel.name = "test-channel"
        mock_bot.get_channel.return_value = mock_channel

        with patch('asyncio.sleep', new_callable=AsyncMock):
            await scheduler._delayed_send(123, "Hello!", 0)

        mock_bot.get_channel.assert_called_once_with(123)
        mock_channel.send.assert_called_once_with("Hello!")

    @pytest.mark.asyncio
    async def test_delayed_send_channel_not_found(self, scheduler, mock_bot):
        """Should not raise when channel is not found."""
        mock_bot.get_channel.return_value = None

        with patch('asyncio.sleep', new_callable=AsyncMock):
            await scheduler._delayed_send(999, "Hello!", 0)

        mock_bot.get_channel.assert_called_once_with(999)
