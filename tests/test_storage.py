"""
Unit tests for FastDC JSONStorage
"""

import json
import os
import pytest
from collections import defaultdict

from fastdc.utils.storage import JSONStorage


@pytest.fixture
def storage_path(tmp_path):
    """Provide a temporary file path for storage tests."""
    return str(tmp_path / "test_data.json")


@pytest.fixture
def storage(storage_path):
    """Provide a fresh JSONStorage instance."""
    return JSONStorage(storage_path)


class TestJSONStorageLoadSave:
    """Tests for loading and saving JSON data."""

    def test_creates_empty_data_when_no_file(self, storage):
        """Should initialize with empty dict when file does not exist."""
        assert storage._data == {}

    def test_load_existing_file(self, storage_path):
        """Should load existing JSON data from file."""
        with open(storage_path, 'w') as f:
            json.dump({"key": "value"}, f)

        s = JSONStorage(storage_path)
        assert s._data == {"key": "value"}

    def test_load_corrupt_file(self, storage_path):
        """Should fallback to empty dict when file contains invalid JSON."""
        with open(storage_path, 'w') as f:
            f.write("not valid json{{{")

        s = JSONStorage(storage_path)
        assert s._data == {}

    def test_save_creates_file(self, storage_path):
        """Should create the file on disk after saving."""
        s = JSONStorage(storage_path)
        s.set("test", 123)
        assert os.path.exists(storage_path)

        with open(storage_path, 'r') as f:
            data = json.load(f)
        assert data["test"] == 123

    def test_save_then_load(self, storage_path):
        """Should persist data across instances."""
        s1 = JSONStorage(storage_path)
        s1.set("hello", "world")

        s2 = JSONStorage(storage_path)
        assert s2.get("hello") == "world"


class TestJSONStorageCRUD:
    """Tests for get, set, and delete operations."""

    def test_get_default(self, storage):
        """Should return None or custom default for missing keys."""
        assert storage.get("missing") is None
        assert storage.get("missing", 42) == 42

    def test_set_and_get(self, storage):
        """Should store and retrieve a value."""
        storage.set("key", "value")
        assert storage.get("key") == "value"

    def test_set_overwrites(self, storage):
        """Should overwrite existing value with same key."""
        storage.set("key", "old")
        storage.set("key", "new")
        assert storage.get("key") == "new"

    def test_delete_existing(self, storage):
        """Should remove an existing key."""
        storage.set("key", "value")
        storage.delete("key")
        assert storage.get("key") is None

    def test_delete_missing_key_no_error(self, storage):
        """Should not raise when deleting a nonexistent key."""
        storage.delete("nonexistent")

    def test_set_complex_data(self, storage):
        """Should handle nested dicts and lists."""
        data = {"nested": {"list": [1, 2, 3], "bool": True}}
        storage.set("complex", data)
        assert storage.get("complex") == data


class TestJSONStorageXP:
    """Tests for XP data persistence."""

    def test_get_xp_data_empty(self, storage):
        """Should return an empty defaultdict when no XP data exists."""
        result = storage.get_xp_data()
        assert isinstance(result, defaultdict)
        assert len(result) == 0

    def test_save_and_get_xp_data(self, storage):
        """Should persist and load XP data correctly."""
        xp = defaultdict(lambda: defaultdict(int))
        xp[123][456] = 500
        xp[123][789] = 1000

        storage.save_xp_data(xp)
        loaded = storage.get_xp_data()

        assert loaded[123][456] == 500
        assert loaded[123][789] == 1000

    def test_xp_data_int_key_conversion(self, storage):
        """Keys stored as strings in JSON should be returned as ints."""
        xp = defaultdict(lambda: defaultdict(int))
        xp[111][222] = 300
        storage.save_xp_data(xp)

        loaded = storage.get_xp_data()
        assert 111 in loaded
        assert 222 in loaded[111]


class TestJSONStorageCustomCommands:
    """Tests for custom commands persistence."""

    def test_get_empty(self, storage):
        """Should return empty dict when no commands saved."""
        assert storage.get_custom_commands() == {}

    def test_save_and_get(self, storage):
        """Should persist and retrieve custom commands."""
        cmds = {"hello": "Hello everyone!", "bye": "Goodbye!"}
        storage.save_custom_commands(cmds)
        assert storage.get_custom_commands() == cmds


class TestJSONStorageAutoReplies:
    """Tests for auto-reply persistence."""

    def test_get_empty(self, storage):
        """Should return empty list when no auto-replies saved."""
        assert storage.get_auto_replies() == []

    def test_save_dict_format(self, storage):
        """Should persist auto-replies provided as dicts."""
        replies = [{"trigger": "hi", "response": "hello"}]
        storage.save_auto_replies(replies)
        loaded = storage.get_auto_replies()
        assert len(loaded) == 1
        assert loaded[0]["trigger"] == "hi"

    def test_save_dataclass_format(self, storage):
        """Should persist auto-replies provided as AutoReplyRule dataclasses."""
        from fastdc.models import AutoReplyRule
        replies = [AutoReplyRule(trigger="bye", response="goodbye")]
        storage.save_auto_replies(replies)
        loaded = storage.get_auto_replies()
        assert len(loaded) == 1
        assert loaded[0]["trigger"] == "bye"
        assert loaded[0]["response"] == "goodbye"


class TestJSONStorageSettings:
    """Tests for settings persistence."""

    def test_get_empty(self, storage):
        """Should return empty dict when no settings saved."""
        assert storage.get_settings() == {}

    def test_save_settings(self, storage):
        """Should persist and retrieve settings."""
        storage.save_settings({"prefix": "?"})
        assert storage.get_settings()["prefix"] == "?"

    def test_save_settings_merge(self, storage):
        """Should merge new settings without overwriting existing ones."""
        storage.save_settings({"prefix": "!"})
        storage.save_settings({"anti_spam": {"action": "warn"}})

        settings = storage.get_settings()
        assert settings["prefix"] == "!"
        assert settings["anti_spam"]["action"] == "warn"
