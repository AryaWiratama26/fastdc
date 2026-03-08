"""
Unit tests for FastDC Custom Exceptions
"""

import pytest
from fastdc.exceptions import FastDCError, ProviderNotConfigured, InvalidProvider


class TestFastDCError:
    """Tests for the base FastDCError exception."""

    def test_is_exception(self):
        """Should be a subclass of Exception."""
        err = FastDCError("test error")
        assert isinstance(err, Exception)

    def test_message(self):
        """Should store the error message correctly."""
        err = FastDCError("something went wrong")
        assert str(err) == "something went wrong"


class TestProviderNotConfigured:
    """Tests for ProviderNotConfigured exception."""

    def test_inherits_from_fastdc_error(self):
        """Should inherit from both FastDCError and Exception."""
        err = ProviderNotConfigured("groq")
        assert isinstance(err, FastDCError)
        assert isinstance(err, Exception)

    def test_message_format(self):
        """Should include provider name and usage hint in message."""
        err = ProviderNotConfigured("groq")
        assert "groq" in str(err)
        assert "not configured" in str(err)
        assert "add_ai_provider()" in str(err)

    def test_different_provider(self):
        """Should correctly embed different provider names."""
        err = ProviderNotConfigured("openai")
        assert "openai" in str(err)


class TestInvalidProvider:
    """Tests for InvalidProvider exception."""

    def test_inherits_from_fastdc_error(self):
        """Should inherit from both FastDCError and Exception."""
        err = InvalidProvider("custom")
        assert isinstance(err, FastDCError)
        assert isinstance(err, Exception)

    def test_message_format(self):
        """Should include provider name and 'Unsupported' in message."""
        err = InvalidProvider("gemini")
        assert "gemini" in str(err)
        assert "Unsupported" in str(err)

    def test_suggests_valid_providers(self):
        """Should mention valid provider options in message."""
        err = InvalidProvider("x")
        msg = str(err)
        assert "groq" in msg or "openai" in msg

    def test_can_be_caught_as_base(self):
        """Should be catchable as FastDCError."""
        with pytest.raises(FastDCError):
            raise InvalidProvider("bad")

    def test_can_be_caught_as_self(self):
        """Should be catchable as InvalidProvider."""
        with pytest.raises(InvalidProvider):
            raise InvalidProvider("bad")
