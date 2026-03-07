"""
FastDC — JSON File Persistence
Saves and loads bot data to/from a JSON file so data survives restarts.
"""

import json
import os
import logging
from collections import defaultdict

logger = logging.getLogger('fastdc.storage')

DEFAULT_FILE = 'fastdc_data.json'


class JSONStorage:
    """
    Simple JSON-backed storage for bot data.
    Auto-saves on every write operation.
    """

    def __init__(self, filepath: str = DEFAULT_FILE):
        self.filepath = filepath
        self._data = {}
        self.load()

    def load(self):
        """Load data from JSON file."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
                logger.info(f"Loaded data from {self.filepath}")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not load {self.filepath}: {e}")
                self._data = {}
        else:
            self._data = {}

    def save(self):
        """Save data to JSON file."""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Could not save {self.filepath}: {e}")

    def get(self, key: str, default=None):
        """Get a value by key."""
        return self._data.get(key, default)

    def set(self, key: str, value):
        """Set a value and auto-save."""
        self._data[key] = value
        self.save()

    def delete(self, key: str):
        """Delete a key and auto-save."""
        if key in self._data:
            del self._data[key]
            self.save()

    def get_xp_data(self):
        """Get XP data as nested defaultdict(int)."""
        raw = self.get('xp_data', {})
        result = defaultdict(lambda: defaultdict(int))
        for guild_id, users in raw.items():
            for user_id, xp in users.items():
                result[int(guild_id)][int(user_id)] = xp
        return result

    def save_xp_data(self, xp_data):
        """Save XP data (convert int keys to strings for JSON)."""
        serializable = {}
        for guild_id, users in xp_data.items():
            serializable[str(guild_id)] = {
                str(user_id): xp for user_id, xp in users.items()
            }
        self.set('xp_data', serializable)

    def get_custom_commands(self):
        """Get custom commands dict."""
        return self.get('custom_commands', {})

    def save_custom_commands(self, commands: dict):
        """Save custom commands."""
        self.set('custom_commands', commands)

    def get_auto_replies(self):
        """Get auto replies as list of dicts."""
        return self.get('auto_replies', [])

    def save_auto_replies(self, replies: list):
        """Save auto replies."""
        self.set('auto_replies', [
            {'trigger': r['trigger'], 'response': r['response']}
            if isinstance(r, dict)
            else {'trigger': r.trigger, 'response': r.response}
            for r in replies
        ])

    def get_settings(self):
        """Get dashboard settings overrides."""
        return self.get('settings', {})

    def save_settings(self, settings: dict):
        """Save settings overrides."""
        current = self.get('settings', {})
        current.update(settings)
        self.set('settings', current)
