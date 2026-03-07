"""
FastDC Embed Builder — Quick helper for creating beautiful embeds
"""

import discord
from typing import Optional, List, Tuple
from datetime import datetime


class QuickEmbed:
    """
    Helper class for creating Discord embeds quickly.
    
    Usage:
        embed = QuickEmbed.build(
            title="Hello!",
            description="Welcome to the server",
            color=QuickEmbed.SUCCESS,
            fields=[("Name", "Value", True)],
            footer="FastDC Bot"
        )
        await ctx.send(embed=embed)
    """

    # Preset colors
    PRIMARY = discord.Color.blue()
    SUCCESS = discord.Color.green()
    WARNING = discord.Color.orange()
    ERROR = discord.Color.red()
    INFO = discord.Color.blurple()
    PURPLE = discord.Color.purple()

    @staticmethod
    def build(
        title: str,
        description: str = "",
        color: discord.Color = None,
        fields: List[Tuple[str, str, bool]] = None,
        thumbnail: str = None,
        image: str = None,
        footer: str = None,
        author_name: str = None,
        author_icon: str = None,
        timestamp: bool = False
    ) -> discord.Embed:
        """
        Build a Discord embed with the given parameters.

        Parameters:
        ----------
        title : str
            The embed title
        description : str
            The embed description
        color : discord.Color
            Embed color (use QuickEmbed.SUCCESS, .ERROR, etc.)
        fields : List[Tuple[str, str, bool]]
            List of (name, value, inline) tuples
        thumbnail : str
            URL for embed thumbnail
        image : str
            URL for embed image
        footer : str
            Footer text
        author_name : str
            Author name
        author_icon : str
            Author icon URL
        timestamp : bool
            Whether to add current timestamp
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=color or QuickEmbed.PRIMARY
        )

        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if image:
            embed.set_image(url=image)

        if footer:
            embed.set_footer(text=footer)

        if author_name:
            embed.set_author(name=author_name, icon_url=author_icon)

        if timestamp:
            embed.timestamp = datetime.now()

        return embed

    @staticmethod
    def success(title: str, description: str = "") -> discord.Embed:
        """Quick success embed (green)"""
        return QuickEmbed.build(title=f"✅ {title}", description=description, color=QuickEmbed.SUCCESS)

    @staticmethod
    def error(title: str, description: str = "") -> discord.Embed:
        """Quick error embed (red)"""
        return QuickEmbed.build(title=f"❌ {title}", description=description, color=QuickEmbed.ERROR)

    @staticmethod
    def warning(title: str, description: str = "") -> discord.Embed:
        """Quick warning embed (orange)"""
        return QuickEmbed.build(title=f"⚠️ {title}", description=description, color=QuickEmbed.WARNING)

    @staticmethod
    def info(title: str, description: str = "") -> discord.Embed:
        """Quick info embed (blurple)"""
        return QuickEmbed.build(title=f"ℹ️ {title}", description=description, color=QuickEmbed.INFO)
