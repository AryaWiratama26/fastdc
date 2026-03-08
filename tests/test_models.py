"""
Unit tests for FastDC Data Models
"""

import pytest
from fastdc.models import (
    AIProvider,
    AutoReplyRule,
    ReactionRoleMapping,
    AntiSpamConfig,
    ScheduledMessage,
)


class TestAIProvider:
    """Tests for the AIProvider dataclass."""

    def test_creation_with_required_fields(self):
        """Should create an AIProvider with only required fields."""
        provider = AIProvider(name="groq", api_key="key123")
        assert provider.name == "groq"
        assert provider.api_key == "key123"
        assert provider.model is None
        assert provider.client is None

    def test_creation_with_all_fields(self):
        """Should create an AIProvider with all fields populated."""
        mock_client = object()
        provider = AIProvider(name="openai", api_key="sk-xxx", model="gpt-4", client=mock_client)
        assert provider.name == "openai"
        assert provider.api_key == "sk-xxx"
        assert provider.model == "gpt-4"
        assert provider.client is mock_client

    def test_model_default_is_none(self):
        """Model field should default to None."""
        provider = AIProvider(name="groq", api_key="key")
        assert provider.model is None

    def test_client_default_is_none(self):
        """Client field should default to None."""
        provider = AIProvider(name="groq", api_key="key")
        assert provider.client is None


class TestAutoReplyRule:
    """Tests for the AutoReplyRule dataclass."""

    def test_creation(self):
        """Should create a rule with trigger and response."""
        rule = AutoReplyRule(trigger="hello", response="Hi there!")
        assert rule.trigger == "hello"
        assert rule.response == "Hi there!"

    def test_trigger_case_preserved(self):
        """Trigger case should be preserved as-is."""
        rule = AutoReplyRule(trigger="Hello", response="Hi")
        assert rule.trigger == "Hello"

    def test_empty_strings(self):
        """Should accept empty strings for trigger and response."""
        rule = AutoReplyRule(trigger="", response="")
        assert rule.trigger == ""
        assert rule.response == ""


class TestReactionRoleMapping:
    """Tests for the ReactionRoleMapping dataclass."""

    def test_creation(self):
        """Should create a mapping with message_id, emoji, and role_id."""
        mapping = ReactionRoleMapping(message_id=123456, emoji="👍", role_id=789012)
        assert mapping.message_id == 123456
        assert mapping.emoji == "👍"
        assert mapping.role_id == 789012

    def test_unicode_emoji(self):
        """Should handle unicode emoji characters."""
        mapping = ReactionRoleMapping(message_id=1, emoji="⭐", role_id=2)
        assert mapping.emoji == "⭐"


class TestAntiSpamConfig:
    """Tests for the AntiSpamConfig dataclass."""

    def test_default_values(self):
        """Should have sensible default values."""
        config = AntiSpamConfig()
        assert config.max_messages == 5
        assert config.interval_seconds == 5
        assert config.action == "mute"
        assert config.mute_duration == 300

    def test_custom_values(self):
        """Should accept custom values for all fields."""
        config = AntiSpamConfig(
            max_messages=10,
            interval_seconds=3,
            action="kick",
            mute_duration=600,
        )
        assert config.max_messages == 10
        assert config.interval_seconds == 3
        assert config.action == "kick"
        assert config.mute_duration == 600

    def test_warn_action(self):
        """Should accept 'warn' as a valid action."""
        config = AntiSpamConfig(action="warn")
        assert config.action == "warn"


class TestScheduledMessage:
    """Tests for the ScheduledMessage dataclass."""

    def test_creation(self):
        """Should create a scheduled message with default task=None."""
        msg = ScheduledMessage(channel_id=123, message="Hello!", delay_seconds=60.0)
        assert msg.channel_id == 123
        assert msg.message == "Hello!"
        assert msg.delay_seconds == 60.0
        assert msg.task is None

    def test_with_task(self):
        """Should store a task reference when provided."""
        mock_task = object()
        msg = ScheduledMessage(channel_id=1, message="Test", delay_seconds=10, task=mock_task)
        assert msg.task is mock_task

    def test_float_delay(self):
        """Should accept fractional delay values."""
        msg = ScheduledMessage(channel_id=1, message="Test", delay_seconds=0.5)
        assert msg.delay_seconds == 0.5
