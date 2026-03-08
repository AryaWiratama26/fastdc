"""
Unit tests for FastDC QuickEmbed Builder
"""

import pytest
import discord

from fastdc.utils.embed_builder import QuickEmbed


class TestQuickEmbedColors:
    """Tests for QuickEmbed color preset constants."""

    def test_primary_is_blue(self):
        """PRIMARY constant should be discord.Color.blue()."""
        assert QuickEmbed.PRIMARY == discord.Color.blue()

    def test_success_is_green(self):
        """SUCCESS constant should be discord.Color.green()."""
        assert QuickEmbed.SUCCESS == discord.Color.green()

    def test_warning_is_orange(self):
        """WARNING constant should be discord.Color.orange()."""
        assert QuickEmbed.WARNING == discord.Color.orange()

    def test_error_is_red(self):
        """ERROR constant should be discord.Color.red()."""
        assert QuickEmbed.ERROR == discord.Color.red()

    def test_info_is_blurple(self):
        """INFO constant should be discord.Color.blurple()."""
        assert QuickEmbed.INFO == discord.Color.blurple()

    def test_purple_is_purple(self):
        """PURPLE constant should be discord.Color.purple()."""
        assert QuickEmbed.PURPLE == discord.Color.purple()


class TestQuickEmbedBuild:
    """Tests for the QuickEmbed.build() static method."""

    def test_basic_embed(self):
        """Should create an Embed with title and description."""
        embed = QuickEmbed.build(title="Test", description="Hello")
        assert isinstance(embed, discord.Embed)
        assert embed.title == "Test"
        assert embed.description == "Hello"

    def test_default_color_is_primary(self):
        """Should use PRIMARY color when no color is specified."""
        embed = QuickEmbed.build(title="Test")
        assert embed.color == QuickEmbed.PRIMARY

    def test_custom_color(self):
        """Should use the provided custom color."""
        embed = QuickEmbed.build(title="Test", color=discord.Color.red())
        assert embed.color == discord.Color.red()

    def test_with_fields(self):
        """Should add fields with correct name, value, and inline settings."""
        fields = [
            ("Field1", "Value1", True),
            ("Field2", "Value2", False),
        ]
        embed = QuickEmbed.build(title="Test", fields=fields)
        assert len(embed.fields) == 2
        assert embed.fields[0].name == "Field1"
        assert embed.fields[0].value == "Value1"
        assert embed.fields[0].inline is True
        assert embed.fields[1].name == "Field2"
        assert embed.fields[1].inline is False

    def test_with_thumbnail(self):
        """Should set the thumbnail URL."""
        embed = QuickEmbed.build(title="Test", thumbnail="https://example.com/img.png")
        assert embed.thumbnail.url == "https://example.com/img.png"

    def test_with_image(self):
        """Should set the image URL."""
        embed = QuickEmbed.build(title="Test", image="https://example.com/img.png")
        assert embed.image.url == "https://example.com/img.png"

    def test_with_footer(self):
        """Should set the footer text."""
        embed = QuickEmbed.build(title="Test", footer="Footer text")
        assert embed.footer.text == "Footer text"

    def test_with_author(self):
        """Should set author name and icon URL."""
        embed = QuickEmbed.build(
            title="Test",
            author_name="Author",
            author_icon="https://example.com/icon.png"
        )
        assert embed.author.name == "Author"
        assert embed.author.icon_url == "https://example.com/icon.png"

    def test_with_timestamp(self):
        """Should set a timestamp when timestamp=True."""
        embed = QuickEmbed.build(title="Test", timestamp=True)
        assert embed.timestamp is not None

    def test_without_timestamp(self):
        """Should not set a timestamp when timestamp=False."""
        embed = QuickEmbed.build(title="Test", timestamp=False)
        assert embed.timestamp is None

    def test_no_fields_by_default(self):
        """Should have no fields when none are provided."""
        embed = QuickEmbed.build(title="Test")
        assert len(embed.fields) == 0

    def test_empty_description(self):
        """Should default to empty description."""
        embed = QuickEmbed.build(title="Test")
        assert embed.description == ""


class TestQuickEmbedPresets:
    """Tests for QuickEmbed shortcut methods (success, error, warning, info)."""

    def test_success(self):
        """Should create a green embed with ✅ prefix."""
        embed = QuickEmbed.success("Done", "Task completed")
        assert "✅" in embed.title
        assert "Done" in embed.title
        assert embed.description == "Task completed"
        assert embed.color == QuickEmbed.SUCCESS

    def test_error(self):
        """Should create a red embed with ❌ prefix."""
        embed = QuickEmbed.error("Oops", "Something broke")
        assert "❌" in embed.title
        assert "Oops" in embed.title
        assert embed.description == "Something broke"
        assert embed.color == QuickEmbed.ERROR

    def test_warning(self):
        """Should create an orange embed with ⚠️ prefix."""
        embed = QuickEmbed.warning("Watch Out", "Be careful")
        assert "⚠️" in embed.title
        assert "Watch Out" in embed.title
        assert embed.color == QuickEmbed.WARNING

    def test_info(self):
        """Should create a blurple embed with ℹ️ prefix."""
        embed = QuickEmbed.info("Note", "FYI")
        assert "ℹ️" in embed.title
        assert "Note" in embed.title
        assert embed.color == QuickEmbed.INFO

    def test_success_empty_desc(self):
        """Should accept empty description for success preset."""
        embed = QuickEmbed.success("Done")
        assert embed.description == ""

    def test_error_empty_desc(self):
        """Should accept empty description for error preset."""
        embed = QuickEmbed.error("Oops")
        assert embed.description == ""
