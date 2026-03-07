"""
FastDC Utility Helpers
"""

import os
from difflib import get_close_matches
from typing import List, Optional

import discord


def find_channel(guild: discord.Guild) -> Optional[discord.TextChannel]:
    """
    Find the best text channel to send a message in a guild.
    Returns the system channel or the first channel the bot can send to.
    """
    channel = guild.system_channel
    if not channel:
        for ch in guild.text_channels:
            if ch.permissions_for(guild.me).send_messages:
                channel = ch
                break
    return channel


def load_knowledge(filepath: str) -> List[str]:
    """
    Read knowledge entries from a text file.
    Entries are separated by double newlines.
    """
    if not filepath or not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().split('\n\n')


def find_relevant_info(question: str, entries: List[str]) -> str:
    """
    Find the most relevant knowledge entries for a question using fuzzy matching.
    Returns up to 2 matched entries as a single string.
    """
    if not entries:
        return ''
    matches = get_close_matches(question, entries, n=2, cutoff=0.2)
    return '\n'.join(matches) if matches else ''
