"""
Unit tests for FastDC Dashboard safe_int and auth
"""

import pytest
from fastdc.dashboard.server import safe_int


class TestSafeInt:
    """Tests for safe_int() utility function."""

    def test_valid_int_string(self):
        """Should parse valid integer strings."""
        assert safe_int("42") == 42

    def test_valid_int(self):
        """Should pass through actual integers."""
        assert safe_int(10) == 10

    def test_invalid_string(self):
        """Should return None for non-numeric strings."""
        assert safe_int("abc") is None

    def test_invalid_with_default(self):
        """Should return custom default for invalid input."""
        assert safe_int("abc", default=0) == 0

    def test_none_value(self):
        """Should return None when input is None."""
        assert safe_int(None) is None

    def test_none_with_default(self):
        """Should return custom default when input is None."""
        assert safe_int(None, default=-1) == -1

    def test_empty_string(self):
        """Should return None for empty string."""
        assert safe_int("") is None

    def test_float_string(self):
        """Should return None for float strings like '3.14'."""
        assert safe_int("3.14") is None

    def test_negative(self):
        """Should parse negative integer strings."""
        assert safe_int("-5") == -5

    def test_zero(self):
        """Should parse zero correctly."""
        assert safe_int("0") == 0

    def test_large_number(self):
        """Should handle large integer values."""
        assert safe_int("999999999") == 999999999
