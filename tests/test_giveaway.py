"""
Unit tests for giveaway/reminder pure functions: parse_duration, format_duration
"""

import pytest

from fastdc.commands.giveaway import parse_duration as giveaway_parse
from fastdc.commands.giveaway import format_duration as giveaway_format
from fastdc.commands.reminder import parse_duration as reminder_parse
from fastdc.commands.reminder import format_duration as reminder_format


class TestGiveawayParseDuration:
    """Tests for parse_duration() from giveaway module."""

    def test_seconds(self):
        """Should parse '30s' as 30 seconds."""
        assert giveaway_parse("30s") == 30

    def test_minutes(self):
        """Should parse '5m' as 300 seconds."""
        assert giveaway_parse("5m") == 300

    def test_hours(self):
        """Should parse '1h' as 3600 seconds."""
        assert giveaway_parse("1h") == 3600

    def test_days(self):
        """Should parse '2d' as 172800 seconds."""
        assert giveaway_parse("2d") == 172800

    def test_uppercase(self):
        """Should handle uppercase unit letters."""
        assert giveaway_parse("10M") == 600

    def test_invalid_format(self):
        """Should return 0 for invalid format strings."""
        assert giveaway_parse("abc") == 0

    def test_empty_string(self):
        """Should return 0 for empty string."""
        assert giveaway_parse("") == 0

    def test_no_unit(self):
        """Should return 0 when no unit suffix is provided."""
        assert giveaway_parse("100") == 0

    def test_negative_not_matched(self):
        """Should return 0 for negative duration strings."""
        assert giveaway_parse("-5m") == 0

    def test_zero(self):
        """Should return 0 for zero duration."""
        assert giveaway_parse("0s") == 0

    def test_large_number(self):
        """Should handle large numbers correctly."""
        assert giveaway_parse("999d") == 999 * 86400


class TestGiveawayFormatDuration:
    """Tests for format_duration() from giveaway module."""

    def test_seconds(self):
        """Should format 30 seconds as '30 second(s)'."""
        assert giveaway_format(30) == "30 second(s)"

    def test_minutes(self):
        """Should format 300 seconds as '5 minute(s)'."""
        assert giveaway_format(300) == "5 minute(s)"

    def test_hours(self):
        """Should format 3600 seconds as '1 hour(s)'."""
        assert giveaway_format(3600) == "1 hour(s)"

    def test_days(self):
        """Should format 86400 seconds as '1 day(s)'."""
        assert giveaway_format(86400) == "1 day(s)"

    def test_multiple_days(self):
        """Should format 172800 seconds as '2 day(s)'."""
        assert giveaway_format(172800) == "2 day(s)"

    def test_59_seconds(self):
        """Should format 59 seconds as '59 second(s)'."""
        assert giveaway_format(59) == "59 second(s)"

    def test_61_seconds_shows_minutes(self):
        """Should format exactly 60 seconds as '1 minute(s)'."""
        assert giveaway_format(60) == "1 minute(s)"


class TestReminderParseDuration:
    """Tests for parse_duration() from reminder module."""

    def test_seconds(self):
        """Should parse '30s' as 30 seconds."""
        assert reminder_parse("30s") == 30

    def test_minutes(self):
        """Should parse '5m' as 300 seconds."""
        assert reminder_parse("5m") == 300

    def test_hours(self):
        """Should parse '1h' as 3600 seconds."""
        assert reminder_parse("1h") == 3600

    def test_days(self):
        """Should parse '2d' as 172800 seconds."""
        assert reminder_parse("2d") == 172800

    def test_invalid(self):
        """Should return 0 for invalid format strings."""
        assert reminder_parse("xyz") == 0


class TestReminderFormatDuration:
    """Tests for format_duration() from reminder module."""

    def test_seconds(self):
        """Should format 45 seconds as '45 second(s)'."""
        assert reminder_format(45) == "45 second(s)"

    def test_minutes(self):
        """Should format 120 seconds as '2 minute(s)'."""
        assert reminder_format(120) == "2 minute(s)"

    def test_hours(self):
        """Should format 7200 seconds as '2 hour(s)'."""
        assert reminder_format(7200) == "2 hour(s)"

    def test_days(self):
        """Should format 259200 seconds as '3 day(s)'."""
        assert reminder_format(259200) == "3 day(s)"
