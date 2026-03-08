"""
Unit tests for FastDC Leveling pure functions: xp_for_level, level_from_xp
"""

import pytest

from fastdc.commands.leveling import xp_for_level, level_from_xp


class TestXpForLevel:
    """Tests for xp_for_level() function."""

    def test_level_0(self):
        """Level 0 should require 0 XP."""
        assert xp_for_level(0) == 0

    def test_level_1(self):
        """Level 1 should require 100 XP."""
        assert xp_for_level(1) == 100

    def test_level_2(self):
        """Level 2 should require 400 XP."""
        assert xp_for_level(2) == 400

    def test_level_5(self):
        """Level 5 should require 2500 XP."""
        assert xp_for_level(5) == 2500

    def test_level_10(self):
        """Level 10 should require 10000 XP."""
        assert xp_for_level(10) == 10000

    def test_formula(self):
        """XP formula should be level² × 100 for all levels."""
        for level in range(20):
            assert xp_for_level(level) == level * level * 100


class TestLevelFromXp:
    """Tests for level_from_xp() function."""

    def test_zero_xp(self):
        """0 XP should be level 0."""
        assert level_from_xp(0) == 0

    def test_99_xp(self):
        """99 XP should still be level 0."""
        assert level_from_xp(99) == 0

    def test_100_xp(self):
        """100 XP should reach level 1."""
        assert level_from_xp(100) == 1

    def test_399_xp(self):
        """399 XP should still be level 1."""
        assert level_from_xp(399) == 1

    def test_400_xp(self):
        """400 XP should reach level 2."""
        assert level_from_xp(400) == 2

    def test_10000_xp(self):
        """10000 XP should reach level 10."""
        assert level_from_xp(10000) == 10

    def test_roundtrip(self):
        """xp_for_level(level_from_xp(xp)) should give the XP threshold for that level."""
        for level in range(15):
            xp = xp_for_level(level)
            assert level_from_xp(xp) == level

    def test_large_xp(self):
        """Should correctly calculate level for large XP values."""
        assert level_from_xp(1000000) == 100


class TestXpLevelConsistency:
    """Tests for consistency between xp_for_level and level_from_xp."""

    def test_level_increases_monotonically(self):
        """Level should never decrease as XP increases."""
        prev_level = -1
        for xp in range(0, 5001, 100):
            level = level_from_xp(xp)
            assert level >= prev_level
            prev_level = level

    def test_xp_for_level_increases(self):
        """XP requirement should always increase with level."""
        for level in range(20):
            assert xp_for_level(level + 1) > xp_for_level(level)
