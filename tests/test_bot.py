"""
Unit tests for FastBot class
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock

from fastdc.bot import FastBot
from fastdc.models import AIProvider, AutoReplyRule, ReactionRoleMapping, AntiSpamConfig
from fastdc.exceptions import InvalidProvider, ProviderNotConfigured


class MockStorage:
    """Lightweight mock for JSONStorage to avoid file I/O."""

    def __init__(self, filepath=None):
        self._data = {}

    def load(self): pass
    def save(self): pass
    def get(self, key, default=None): return self._data.get(key, default)
    def set(self, key, value): self._data[key] = value
    def delete(self, key): self._data.pop(key, None)
    def get_custom_commands(self): return {}
    def get_xp_data(self): return {}
    def get_auto_replies(self): return []
    def get_settings(self): return {}
    def save_custom_commands(self, data): pass
    def save_auto_replies(self, data): pass
    def save_xp_data(self, data): pass
    def save_settings(self, data): pass


@pytest.fixture
def bot():
    """Create a FastBot instance with mocked storage and discord bot."""
    with patch('fastdc.bot.JSONStorage', MockStorage):
        with patch('fastdc.bot.commands.Bot'):
            return FastBot(token="test-token")


class TestFastBotInit:
    """Tests for FastBot initialization."""

    def test_default_values(self, bot):
        """Should initialize with sensible default values."""
        assert bot.token == "test-token"
        assert bot.ai_providers == {}
        assert bot.auto_replies == []
        assert bot.reaction_roles == []
        assert isinstance(bot.anti_spam_config, AntiSpamConfig)
        assert bot.scheduler is None
        assert bot._has_anti_spam is False
        assert bot._has_leveling is False
        assert bot._button_role_configs == []

    def test_custom_prefix(self):
        """Should pass custom prefix to the discord.ext.commands.Bot."""
        with patch('fastdc.bot.JSONStorage', MockStorage):
            with patch('fastdc.bot.commands.Bot') as MockBot:
                bot = FastBot(token="t", prefix="?")
                MockBot.assert_called_once()
                call_kwargs = MockBot.call_args
                assert call_kwargs[1]['command_prefix'] == '?' or call_kwargs.kwargs['command_prefix'] == '?'

    def test_welcome_defaults(self, bot):
        """Should have welcome/leave features disabled by default."""
        assert bot._welcome_enabled is False
        assert bot._welcome_message == "Hello {member}, welcome to Server!"
        assert bot._leave_enabled is False


class TestFastBotAIProvider:
    """Tests for add_ai_provider() method."""

    def test_add_groq_provider(self, bot):
        """Should register a groq provider in the ai_providers dict."""
        with patch('fastdc.bot.FastBot.add_ai_provider') as mock:
            mock.side_effect = lambda p, k, **kw: bot.ai_providers.__setitem__(
                p, AIProvider(name=p, api_key=k)
            )
            bot.add_ai_provider("groq", "key123")
            assert "groq" in bot.ai_providers

    def test_invalid_provider(self, bot):
        """Should raise InvalidProvider for unsupported provider names."""
        with pytest.raises(InvalidProvider):
            bot.add_ai_provider("gemini", "key")


class TestFastBotAIChat:
    """Tests for ai_chat() method."""

    def test_provider_not_configured(self, bot):
        """Should raise ProviderNotConfigured when provider is not added."""
        with pytest.raises(ProviderNotConfigured):
            bot.ai_chat(provider="groq")


class TestFastBotAutoReply:
    """Tests for auto_reply() method."""

    def test_add_auto_reply(self, bot):
        """Should add an AutoReplyRule to the auto_replies list."""
        bot.auto_reply("hello", "hi there!")
        assert len(bot.auto_replies) == 1
        assert bot.auto_replies[0].trigger == "hello"
        assert bot.auto_replies[0].response == "hi there!"

    def test_trigger_lowercased(self, bot):
        """Should lowercase the trigger for case-insensitive matching."""
        bot.auto_reply("HELLO", "hi")
        assert bot.auto_replies[0].trigger == "hello"

    def test_multiple_replies(self, bot):
        """Should accumulate multiple auto-reply rules."""
        bot.auto_reply("hi", "hello")
        bot.auto_reply("bye", "goodbye")
        assert len(bot.auto_replies) == 2


class TestFastBotReactionRole:
    """Tests for add_reaction_role() method."""

    def test_add_reaction_role(self, bot):
        """Should add a ReactionRoleMapping to the reaction_roles list."""
        bot.add_reaction_role(message_id=123, emoji="👍", role_id=456)
        assert len(bot.reaction_roles) == 1
        mapping = bot.reaction_roles[0]
        assert isinstance(mapping, ReactionRoleMapping)
        assert mapping.message_id == 123
        assert mapping.emoji == "👍"
        assert mapping.role_id == 456

    def test_multiple_reaction_roles(self, bot):
        """Should accumulate multiple reaction role mappings."""
        bot.add_reaction_role(1, "👍", 10)
        bot.add_reaction_role(2, "👎", 20)
        assert len(bot.reaction_roles) == 2


class TestFastBotAntiSpam:
    """Tests for enable_anti_spam() method."""

    def test_enable_with_defaults(self, bot):
        """Should enable anti-spam with default config values."""
        bot.enable_anti_spam()
        assert bot._has_anti_spam is True
        assert bot.anti_spam_config.max_messages == 5
        assert bot.anti_spam_config.interval_seconds == 5
        assert bot.anti_spam_config.action == "mute"
        assert bot.anti_spam_config.mute_duration == 300

    def test_enable_with_custom(self, bot):
        """Should accept custom anti-spam configuration."""
        bot.enable_anti_spam(max_messages=10, interval=3, action="kick", mute_duration=600)
        assert bot.anti_spam_config.max_messages == 10
        assert bot.anti_spam_config.interval_seconds == 3
        assert bot.anti_spam_config.action == "kick"
        assert bot.anti_spam_config.mute_duration == 600


class TestFastBotButtonRole:
    """Tests for add_button_role() method."""

    def test_add_button_role(self, bot):
        """Should add a button role config to the list."""
        bot.add_button_role(role_id=111, label="Gamer", emoji="🎮")
        assert len(bot._button_role_configs) == 1
        cfg = bot._button_role_configs[0]
        assert cfg['role_id'] == 111
        assert cfg['label'] == "Gamer"
        assert cfg['emoji'] == "🎮"
        assert cfg['style'] == "primary"

    def test_custom_style(self, bot):
        """Should accept custom button styles."""
        bot.add_button_role(role_id=222, label="X", style="danger")
        assert bot._button_role_configs[0]['style'] == "danger"

    def test_multiple_buttons(self, bot):
        """Should accumulate multiple button configs."""
        bot.add_button_role(role_id=1, label="A")
        bot.add_button_role(role_id=2, label="B")
        assert len(bot._button_role_configs) == 2


class TestFastBotPresence:
    """Tests for set_presence() method."""

    def test_set_presence(self, bot):
        """Should store custom presence settings."""
        bot.set_presence(status="dnd", activity_type="watching", activity_name="Test")
        assert bot._presence_status == "dnd"
        assert bot._presence_activity_type == "watching"
        assert bot._presence_activity_name == "Test"

    def test_default_presence(self, bot):
        """Should use default presence values when not specified."""
        bot.set_presence()
        assert bot._presence_status == "online"
        assert bot._presence_activity_type == "playing"
        assert bot._presence_activity_name == "FastDC Bot"


class TestFastBotScheduleMessage:
    """Tests for schedule_message() method."""

    def test_creates_scheduler(self, bot):
        """Should create a MessageScheduler on first call."""
        with patch('fastdc.bot.MessageScheduler') as MockScheduler:
            instance = MockScheduler.return_value
            instance.schedule.return_value = MagicMock()
            bot.schedule_message(channel_id=123, message="Hi", delay_seconds=60)
            assert bot.scheduler is instance

    def test_uses_existing_scheduler(self, bot):
        """Should reuse existing scheduler for subsequent calls."""
        mock_scheduler = MagicMock()
        bot.scheduler = mock_scheduler
        bot.schedule_message(channel_id=123, message="Hi", delay_seconds=60)
        mock_scheduler.schedule.assert_called_once_with(123, "Hi", 60)


class TestFastBotStaticMethods:
    """Tests for FastBot static/class methods."""

    def test_quick_embed(self):
        """Should return a discord.Embed via QuickEmbed."""
        import discord
        embed = FastBot.quick_embed("Hello", "World")
        assert isinstance(embed, discord.Embed)
        assert embed.title == "Hello"

    @pytest.mark.asyncio
    async def test_paginate(self):
        """Should return an EmbedPaginator with the given pages."""
        import discord
        from fastdc.utils.paginator import EmbedPaginator
        pages = [discord.Embed(title=f"P{i}") for i in range(3)]
        paginator = FastBot.paginate(pages)
        assert isinstance(paginator, EmbedPaginator)
        assert len(paginator.pages) == 3


class TestFastBotSaveState:
    """Tests for save_state() method."""

    def test_save_state_calls_storage(self, bot):
        """Should call all storage save methods."""
        bot.storage = MagicMock()
        bot._custom_commands = {"test": "hello"}
        bot.auto_replies = [AutoReplyRule(trigger="hi", response="hello")]
        bot._xp_data = {1: {2: 100}}

        bot.save_state()

        bot.storage.save_custom_commands.assert_called_once()
        bot.storage.save_auto_replies.assert_called_once()
        bot.storage.save_xp_data.assert_called_once()


class TestFastBotLeveling:
    """Tests for enable_leveling() method."""

    def test_enable_leveling(self, bot):
        """Should enable leveling with custom XP per message."""
        with patch('fastdc.bot.setup_leveling_system'):
            bot.enable_leveling(xp_per_message=25)
            assert bot._has_leveling is True
            assert bot._xp_per_message == 25

    def test_default_xp(self, bot):
        """Should default to 15 XP per message."""
        with patch('fastdc.bot.setup_leveling_system'):
            bot.enable_leveling()
            assert bot._xp_per_message == 15
