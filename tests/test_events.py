"""
Unit tests for FastDC Event setup functions.
Verifies that calling each setup function registers event handlers on the bot.
"""

import pytest
from unittest.mock import MagicMock
from collections import defaultdict


def make_mock_bot_instance():
    """Create a minimal mock bot instance for event setup tests."""
    bot_instance = MagicMock()

    inner_bot = MagicMock()
    inner_bot.commands = []
    inner_bot.tree = MagicMock()
    bot_instance.bot = inner_bot

    bot_instance.ai_providers = {}
    bot_instance.auto_replies = []
    bot_instance.reaction_roles = []
    bot_instance.anti_spam_config = MagicMock()
    bot_instance.anti_spam_config.max_messages = 5
    bot_instance.anti_spam_config.interval_seconds = 5
    bot_instance.anti_spam_config.action = "warn"
    bot_instance._has_anti_spam = False
    bot_instance._has_leveling = False
    bot_instance._button_role_configs = []
    bot_instance._custom_commands = {}
    bot_instance._xp_data = defaultdict(lambda: defaultdict(int))
    bot_instance._xp_per_message = 15

    return bot_instance


class TestSetupEventLogging:
    """Tests for setup_event_logging() registration."""

    def test_registers_event(self):
        """Should register event handlers on the bot."""
        from fastdc.events.logging import setup_event_logging
        bot_instance = make_mock_bot_instance()
        setup_event_logging(bot_instance)

        bot = bot_instance.bot
        assert bot.event.called


class TestSetupWelcome:
    """Tests for setup_welcome() registration."""

    def test_registers_event(self):
        """Should register the on_member_join event handler."""
        from fastdc.events.welcome import setup_welcome
        bot_instance = make_mock_bot_instance()
        setup_welcome(bot_instance)
        assert bot_instance.bot.event.called

    def test_custom_message(self):
        """Should accept a custom welcome message template."""
        from fastdc.events.welcome import setup_welcome
        bot_instance = make_mock_bot_instance()
        setup_welcome(bot_instance, message="Welcome {member}!")
        assert bot_instance.bot.event.called


class TestSetupLeave:
    """Tests for setup_leave() registration."""

    def test_registers_event(self):
        """Should register the on_member_remove event handler."""
        from fastdc.events.welcome import setup_leave
        bot_instance = make_mock_bot_instance()
        setup_leave(bot_instance)
        assert bot_instance.bot.event.called

    def test_custom_message(self):
        """Should accept a custom leave message template."""
        from fastdc.events.welcome import setup_leave
        bot_instance = make_mock_bot_instance()
        setup_leave(bot_instance, message="Goodbye {member}")
        assert bot_instance.bot.event.called


class TestSetupAutoReply:
    """Tests for setup_auto_reply() registration."""

    def test_registers_event(self):
        """Should register the on_message event handler."""
        from fastdc.events.auto_reply import setup_auto_reply
        bot_instance = make_mock_bot_instance()
        setup_auto_reply(bot_instance)
        assert bot_instance.bot.event.called


class TestSetupReactionRoles:
    """Tests for setup_reaction_roles() registration."""

    def test_registers_event(self):
        """Should register reaction add/remove event handlers."""
        from fastdc.events.reaction_roles import setup_reaction_roles
        bot_instance = make_mock_bot_instance()
        setup_reaction_roles(bot_instance)
        assert bot_instance.bot.event.called


class TestSetupAntiSpam:
    """Tests for setup_anti_spam() registration."""

    def test_registers_event(self):
        """Should register the on_message event handler for spam detection."""
        from fastdc.events.anti_spam import setup_anti_spam
        bot_instance = make_mock_bot_instance()
        setup_anti_spam(bot_instance)
        assert bot_instance.bot.event.called

    def test_with_custom_config(self):
        """Should accept a custom AntiSpamConfig."""
        from fastdc.events.anti_spam import setup_anti_spam
        from fastdc.models import AntiSpamConfig
        bot_instance = make_mock_bot_instance()
        config = AntiSpamConfig(max_messages=10, action="kick")
        setup_anti_spam(bot_instance, config=config)
        assert bot_instance.bot.event.called


class TestSetupAutoRole:
    """Tests for setup_auto_role() registration."""

    def test_registers_event(self):
        """Should register the on_member_join event handler for auto-role."""
        from fastdc.events.auto_role import setup_auto_role
        bot_instance = make_mock_bot_instance()
        setup_auto_role(bot_instance, role_id=123456)
        assert bot_instance.bot.event.called


class TestSetupAFK:
    """Tests for setup_afk_system() registration."""

    def test_registers_commands(self):
        """Should register both prefix and slash AFK commands."""
        from fastdc.events.afk import setup_afk_system
        bot_instance = make_mock_bot_instance()
        setup_afk_system(bot_instance)

        bot = bot_instance.bot
        assert bot.command.called
        assert bot.tree.command.called

    def test_sets_afk_users(self):
        """Should set the _afk_users attribute on bot_instance."""
        from fastdc.events.afk import setup_afk_system
        bot_instance = make_mock_bot_instance()
        setup_afk_system(bot_instance)
        assert hasattr(bot_instance, '_afk_users')


class TestSetupStarboard:
    """Tests for setup_starboard() registration."""

    def test_registers_event(self):
        """Should register the on_raw_reaction_add event handler."""
        from fastdc.events.starboard import setup_starboard
        bot_instance = make_mock_bot_instance()
        setup_starboard(bot_instance, channel_id=123456)
        assert bot_instance.bot.event.called

    def test_custom_config(self):
        """Should accept custom emoji and threshold."""
        from fastdc.events.starboard import setup_starboard
        bot_instance = make_mock_bot_instance()
        setup_starboard(bot_instance, channel_id=123, emoji="🌟", threshold=5)
        assert bot_instance.bot.event.called


class TestSetupTempVoice:
    """Tests for setup_temp_voice() registration."""

    def test_registers_event(self):
        """Should register the on_voice_state_update event handler."""
        from fastdc.events.temp_voice import setup_temp_voice
        bot_instance = make_mock_bot_instance()
        setup_temp_voice(bot_instance, trigger_channel_id=123)
        assert bot_instance.bot.event.called

    def test_with_category(self):
        """Should accept an optional category_id parameter."""
        from fastdc.events.temp_voice import setup_temp_voice
        bot_instance = make_mock_bot_instance()
        setup_temp_voice(bot_instance, trigger_channel_id=123, category_id=456)
        assert bot_instance.bot.event.called


class TestSetupButtonRoles:
    """Tests for setup_button_roles() registration."""

    def test_registers_commands(self):
        """Should register both prefix and slash rolepanel commands."""
        from fastdc.events.button_roles import setup_button_roles
        bot_instance = make_mock_bot_instance()
        setup_button_roles(bot_instance)

        bot = bot_instance.bot
        assert bot.command.called
        assert bot.tree.command.called


class TestRoleButton:
    """Tests for RoleButton UI component."""

    def test_initialization(self):
        """Should store role_id and set custom_id based on role_id."""
        import discord
        from fastdc.events.button_roles import RoleButton
        btn = RoleButton(role_id=123, label="Test", emoji="🎮")
        assert btn.role_id == 123
        assert btn.label == "Test"
        assert btn.custom_id == "role_123"


class TestRoleSelectMenu:
    """Tests for RoleSelectMenu UI component."""

    def test_initialization(self):
        """Should create select options from roles list."""
        from fastdc.events.button_roles import RoleSelectMenu
        roles = [
            (111, "Gamer", "🎮"),
            (222, "Artist", "🎨"),
        ]
        menu = RoleSelectMenu(roles)
        assert len(menu.options) == 2
        assert menu.custom_id == "role_select"


class TestRoleView:
    """Tests for RoleView persistent view."""

    @pytest.mark.asyncio
    async def test_initialization(self):
        """Should have no timeout for persistent role views."""
        from fastdc.events.button_roles import RoleView
        view = RoleView()
        assert view.timeout is None
