"""
FastDC Data Models
"""

from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class AIProvider:
    """Represents a configured AI provider"""
    name: str
    api_key: str
    model: Optional[str] = None
    client: Any = None


@dataclass
class AutoReplyRule:
    """Represents an auto-reply trigger/response pair"""
    trigger: str
    response: str


@dataclass
class ReactionRoleMapping:
    """Maps a message reaction to a role"""
    message_id: int
    emoji: str
    role_id: int


@dataclass
class AntiSpamConfig:
    """Configuration for anti-spam detection"""
    max_messages: int = 5
    interval_seconds: int = 5
    action: str = "mute"  # "mute", "kick", "warn"
    mute_duration: int = 300  # seconds


@dataclass
class ScheduledMessage:
    """Represents a scheduled message"""
    channel_id: int
    message: str
    delay_seconds: float
    task: Any = None
