"""
Unit tests for FastDC EmbedPaginator.
All tests are async because discord.ui.View requires a running event loop.
"""

import pytest
import discord
from unittest.mock import MagicMock, AsyncMock

from fastdc.utils.paginator import EmbedPaginator


def make_embeds(n):
    """Create n dummy embeds for testing."""
    return [discord.Embed(title=f"Page {i+1}") for i in range(n)]


class TestEmbedPaginatorInit:
    """Tests for EmbedPaginator initialization."""

    @pytest.mark.asyncio
    async def test_initialization(self):
        """Should store pages and start at page 0."""
        pages = make_embeds(3)
        pag = EmbedPaginator(pages)
        assert pag.pages == pages
        assert pag.current_page == 0

    @pytest.mark.asyncio
    async def test_custom_timeout(self):
        """Should accept a custom timeout value."""
        pag = EmbedPaginator(make_embeds(2), timeout=60)
        assert pag.timeout == 60

    @pytest.mark.asyncio
    async def test_default_timeout(self):
        """Should default to 120 seconds timeout."""
        pag = EmbedPaginator(make_embeds(2))
        assert pag.timeout == 120

    @pytest.mark.asyncio
    async def test_single_page_buttons_disabled(self):
        """All navigation buttons should be disabled for single-page paginator."""
        pag = EmbedPaginator(make_embeds(1))
        assert pag.first_page.disabled is True
        assert pag.prev_page.disabled is True
        assert pag.next_page.disabled is True
        assert pag.last_page.disabled is True

    @pytest.mark.asyncio
    async def test_multi_page_initial_state(self):
        """Previous buttons should be disabled, next buttons enabled at first page."""
        pag = EmbedPaginator(make_embeds(3))
        assert pag.first_page.disabled is True
        assert pag.prev_page.disabled is True
        assert pag.next_page.disabled is False
        assert pag.last_page.disabled is False


class TestEmbedPaginatorUpdateButtons:
    """Tests for the _update_buttons() method."""

    @pytest.mark.asyncio
    async def test_page_counter_label_first(self):
        """Page counter should show '1/5' at first page."""
        pag = EmbedPaginator(make_embeds(5))
        assert pag.page_counter.label == "1/5"

    @pytest.mark.asyncio
    async def test_page_counter_label_middle(self):
        """Page counter should show '3/5' at middle page."""
        pag = EmbedPaginator(make_embeds(5))
        pag.current_page = 2
        pag._update_buttons()
        assert pag.page_counter.label == "3/5"

    @pytest.mark.asyncio
    async def test_page_counter_label_last(self):
        """Page counter should show '5/5' at last page."""
        pag = EmbedPaginator(make_embeds(5))
        pag.current_page = 4
        pag._update_buttons()
        assert pag.page_counter.label == "5/5"

    @pytest.mark.asyncio
    async def test_buttons_at_last_page(self):
        """Next buttons should be disabled, previous enabled at last page."""
        pag = EmbedPaginator(make_embeds(3))
        pag.current_page = 2
        pag._update_buttons()
        assert pag.first_page.disabled is False
        assert pag.prev_page.disabled is False
        assert pag.next_page.disabled is True
        assert pag.last_page.disabled is True

    @pytest.mark.asyncio
    async def test_buttons_at_middle_page(self):
        """All navigation buttons should be enabled at middle page."""
        pag = EmbedPaginator(make_embeds(3))
        pag.current_page = 1
        pag._update_buttons()
        assert pag.first_page.disabled is False
        assert pag.prev_page.disabled is False
        assert pag.next_page.disabled is False
        assert pag.last_page.disabled is False


class TestEmbedPaginatorNavigation:
    """Tests for page navigation button callbacks."""

    @pytest.mark.asyncio
    async def test_next_page(self):
        """Should advance to the next page."""
        pag = EmbedPaginator(make_embeds(3))
        interaction = MagicMock()
        interaction.response = MagicMock()
        interaction.response.edit_message = AsyncMock()

        await pag.next_page.callback(interaction)
        assert pag.current_page == 1

    @pytest.mark.asyncio
    async def test_prev_page(self):
        """Should go back to the previous page."""
        pag = EmbedPaginator(make_embeds(3))
        pag.current_page = 2
        interaction = MagicMock()
        interaction.response = MagicMock()
        interaction.response.edit_message = AsyncMock()

        await pag.prev_page.callback(interaction)
        assert pag.current_page == 1

    @pytest.mark.asyncio
    async def test_first_page(self):
        """Should jump to the first page."""
        pag = EmbedPaginator(make_embeds(5))
        pag.current_page = 3
        interaction = MagicMock()
        interaction.response = MagicMock()
        interaction.response.edit_message = AsyncMock()

        await pag.first_page.callback(interaction)
        assert pag.current_page == 0

    @pytest.mark.asyncio
    async def test_last_page(self):
        """Should jump to the last page."""
        pag = EmbedPaginator(make_embeds(5))
        interaction = MagicMock()
        interaction.response = MagicMock()
        interaction.response.edit_message = AsyncMock()

        await pag.last_page.callback(interaction)
        assert pag.current_page == 4

    @pytest.mark.asyncio
    async def test_prev_page_clamp_at_zero(self):
        """Should not go below page 0."""
        pag = EmbedPaginator(make_embeds(3))
        pag.current_page = 0
        interaction = MagicMock()
        interaction.response = MagicMock()
        interaction.response.edit_message = AsyncMock()

        await pag.prev_page.callback(interaction)
        assert pag.current_page == 0

    @pytest.mark.asyncio
    async def test_next_page_clamp_at_max(self):
        """Should not go beyond the last page."""
        pag = EmbedPaginator(make_embeds(3))
        pag.current_page = 2
        interaction = MagicMock()
        interaction.response = MagicMock()
        interaction.response.edit_message = AsyncMock()

        await pag.next_page.callback(interaction)
        assert pag.current_page == 2
