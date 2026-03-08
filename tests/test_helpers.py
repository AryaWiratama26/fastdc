"""
Unit tests for FastDC Utility Helpers
"""

import os
import tempfile
import pytest
from unittest.mock import MagicMock, PropertyMock

import discord

from fastdc.utils.helpers import find_channel, load_knowledge, find_relevant_info


class TestFindChannel:
    """Tests for find_channel() helper."""

    def _make_channel(self, name, can_send=True):
        """Create a mock TextChannel."""
        ch = MagicMock(spec=discord.TextChannel)
        ch.name = name
        perms = MagicMock()
        perms.send_messages = can_send
        ch.permissions_for.return_value = perms
        return ch

    def test_returns_system_channel(self):
        """Should return guild.system_channel when available."""
        guild = MagicMock(spec=discord.Guild)
        sys_ch = self._make_channel("system")
        guild.system_channel = sys_ch
        guild.text_channels = [self._make_channel("general")]

        result = find_channel(guild)
        assert result is sys_ch

    def test_fallback_to_first_sendable(self):
        """Should fall back to the first sendable text channel."""
        guild = MagicMock(spec=discord.Guild)
        guild.system_channel = None
        ch1 = self._make_channel("no-perms", can_send=False)
        ch2 = self._make_channel("general", can_send=True)
        guild.text_channels = [ch1, ch2]

        result = find_channel(guild)
        assert result is ch2

    def test_returns_none_when_no_channel(self):
        """Should return None when guild has no text channels."""
        guild = MagicMock(spec=discord.Guild)
        guild.system_channel = None
        guild.text_channels = []

        result = find_channel(guild)
        assert result is None

    def test_returns_none_when_no_sendable_channel(self):
        """Should return None when bot cannot send to any channel."""
        guild = MagicMock(spec=discord.Guild)
        guild.system_channel = None
        ch = self._make_channel("locked", can_send=False)
        guild.text_channels = [ch]

        result = find_channel(guild)
        assert result is None


class TestLoadKnowledge:
    """Tests for load_knowledge() helper."""

    def test_valid_file(self, tmp_path):
        """Should split file content by double newlines."""
        f = tmp_path / "data.txt"
        f.write_text("Entry One\n\nEntry Two\n\nEntry Three")

        entries = load_knowledge(str(f))
        assert len(entries) == 3
        assert entries[0] == "Entry One"
        assert entries[1] == "Entry Two"
        assert entries[2] == "Entry Three"

    def test_file_not_found(self):
        """Should return empty list for nonexistent file."""
        entries = load_knowledge("/nonexistent/path.txt")
        assert entries == []

    def test_none_filepath(self):
        """Should return empty list when filepath is None."""
        entries = load_knowledge(None)
        assert entries == []

    def test_empty_string_filepath(self):
        """Should return empty list when filepath is empty string."""
        entries = load_knowledge("")
        assert entries == []

    def test_empty_file(self, tmp_path):
        """Should return a list with one empty string for an empty file."""
        f = tmp_path / "empty.txt"
        f.write_text("")

        entries = load_knowledge(str(f))
        assert entries == [""]

    def test_single_entry(self, tmp_path):
        """Should return a single entry when no double-newline separator exists."""
        f = tmp_path / "single.txt"
        f.write_text("Only one entry here")

        entries = load_knowledge(str(f))
        assert len(entries) == 1
        assert entries[0] == "Only one entry here"


class TestFindRelevantInfo:
    """Tests for find_relevant_info() helper."""

    def test_empty_entries(self):
        """Should return empty string for empty entries list."""
        result = find_relevant_info("question", [])
        assert result == ""

    def test_matching_entries(self):
        """Should return non-empty string when entries match the question."""
        entries = [
            "Python is a programming language",
            "JavaScript is used for web development",
            "Python can be used for data science",
        ]
        result = find_relevant_info("Python programming", entries)
        assert result != ""

    def test_no_match(self):
        """Should still return a string type even when nothing matches."""
        entries = ["aaaa", "bbbb", "cccc"]
        result = find_relevant_info("zzzzzzzzzzzz completely unrelated xyzxyz", entries)
        assert isinstance(result, str)

    def test_returns_string(self):
        """Should always return a string."""
        result = find_relevant_info("test", ["test entry"])
        assert isinstance(result, str)
