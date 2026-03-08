"""
Unit tests for FastDC Command setup functions.
Verifies that calling each setup function registers commands/slash commands on the bot.
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from collections import defaultdict

from fastdc.models import AIProvider


def make_mock_bot_instance():
    """Create a minimal mock bot instance for setup tests."""
    bot_instance = MagicMock()

    inner_bot = MagicMock()
    inner_bot.commands = []
    inner_bot.tree = MagicMock()
    bot_instance.bot = inner_bot

    bot_instance.ai_providers = {}
    bot_instance.auto_replies = []
    bot_instance.reaction_roles = []
    bot_instance.anti_spam_config = MagicMock()
    bot_instance._has_anti_spam = False
    bot_instance._has_leveling = False
    bot_instance._button_role_configs = []
    bot_instance._custom_commands = {}
    bot_instance._xp_data = defaultdict(lambda: defaultdict(int))
    bot_instance._xp_per_message = 15
    bot_instance._afk_users = {}

    return bot_instance


class TestSetupModeration:
    """Tests for setup_moderation_commands() registration."""

    def test_registers_commands(self):
        """Should register both prefix and slash commands."""
        from fastdc.commands.moderation import setup_moderation_commands
        bot_instance = make_mock_bot_instance()
        setup_moderation_commands(bot_instance)

        bot = bot_instance.bot
        assert bot.command.called
        assert bot.tree.command.called


class TestSetupUtility:
    """Tests for setup_utility_commands() and setup_help() registration."""

    def test_registers_commands(self):
        """Should register both prefix and slash commands."""
        from fastdc.commands.utility import setup_utility_commands
        bot_instance = make_mock_bot_instance()
        setup_utility_commands(bot_instance)

        bot = bot_instance.bot
        assert bot.command.called
        assert bot.tree.command.called

    def test_setup_help(self):
        """Should register help command group."""
        from fastdc.commands.utility import setup_help
        bot_instance = make_mock_bot_instance()
        setup_help(bot_instance)

        bot = bot_instance.bot
        assert bot.group.called or bot.tree.command.called


class TestSetupPoll:
    """Tests for setup_poll_commands() registration."""

    def test_registers_commands(self):
        """Should register both prefix and slash commands."""
        from fastdc.commands.poll import setup_poll_commands
        bot_instance = make_mock_bot_instance()
        setup_poll_commands(bot_instance)

        bot = bot_instance.bot
        assert bot.command.called
        assert bot.tree.command.called


class TestSetupTicket:
    """Tests for setup_ticket_commands() registration."""

    def test_registers_commands(self):
        """Should register both prefix and slash commands."""
        from fastdc.commands.ticket import setup_ticket_commands
        bot_instance = make_mock_bot_instance()
        setup_ticket_commands(bot_instance)

        bot = bot_instance.bot
        assert bot.command.called
        assert bot.tree.command.called


class TestSetupGiveaway:
    """Tests for setup_giveaway_commands() registration."""

    def test_registers_commands(self):
        """Should register both prefix and slash commands."""
        from fastdc.commands.giveaway import setup_giveaway_commands
        bot_instance = make_mock_bot_instance()
        setup_giveaway_commands(bot_instance)

        bot = bot_instance.bot
        assert bot.command.called
        assert bot.tree.command.called


class TestSetupReminder:
    """Tests for setup_reminder_commands() registration."""

    def test_registers_commands(self):
        """Should register both prefix and slash commands."""
        from fastdc.commands.reminder import setup_reminder_commands
        bot_instance = make_mock_bot_instance()
        setup_reminder_commands(bot_instance)

        bot = bot_instance.bot
        assert bot.command.called
        assert bot.tree.command.called


class TestSetupCustomCommands:
    """Tests for setup_custom_commands() registration."""

    def test_registers_commands(self):
        """Should register both prefix and slash commands."""
        from fastdc.commands.custom_commands import setup_custom_commands
        bot_instance = make_mock_bot_instance()
        setup_custom_commands(bot_instance)

        bot = bot_instance.bot
        assert bot.command.called
        assert bot.tree.command.called

    def test_sets_custom_commands_dict(self):
        """Should set the _custom_commands attribute on bot_instance."""
        from fastdc.commands.custom_commands import setup_custom_commands
        bot_instance = make_mock_bot_instance()
        setup_custom_commands(bot_instance)
        assert hasattr(bot_instance, '_custom_commands')


class TestSetupLeveling:
    """Tests for setup_leveling_system() registration."""

    def test_registers_commands(self):
        """Should register both prefix and slash commands."""
        from fastdc.commands.leveling import setup_leveling_system
        bot_instance = make_mock_bot_instance()
        setup_leveling_system(bot_instance)

        bot = bot_instance.bot
        assert bot.command.called
        assert bot.tree.command.called

    def test_sets_xp_data(self):
        """Should set the _xp_data attribute on bot_instance."""
        from fastdc.commands.leveling import setup_leveling_system
        bot_instance = make_mock_bot_instance()
        setup_leveling_system(bot_instance)
        assert hasattr(bot_instance, '_xp_data')


class TestSetupAI:
    """Tests for setup_ai_commands() registration."""

    def test_registers_commands(self):
        """Should register both prefix and slash commands."""
        from fastdc.commands.ai import setup_ai_commands
        bot_instance = make_mock_bot_instance()
        mock_client = MagicMock()
        bot_instance.ai_providers = {
            "groq": AIProvider(name="groq", api_key="key", model=None, client=mock_client)
        }
        setup_ai_commands(bot_instance, provider="groq")

        bot = bot_instance.bot
        assert bot.command.called
        assert bot.tree.command.called

    def test_with_context_file(self):
        """Should accept an optional context_file parameter without raising."""
        from fastdc.commands.ai import setup_ai_commands
        bot_instance = make_mock_bot_instance()
        mock_client = MagicMock()
        bot_instance.ai_providers = {
            "groq": AIProvider(name="groq", api_key="key", model=None, client=mock_client)
        }
        setup_ai_commands(bot_instance, provider="groq", context_file="data.txt")
