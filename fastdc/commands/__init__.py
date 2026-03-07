from .ai import setup_ai_commands
from .moderation import setup_moderation_commands
from .utility import setup_utility_commands, setup_help
from .poll import setup_poll_commands
from .ticket import setup_ticket_commands
from .giveaway import setup_giveaway_commands
from .reminder import setup_reminder_commands
from .custom_commands import setup_custom_commands
from .leveling import setup_leveling_system

__all__ = [
    'setup_ai_commands',
    'setup_moderation_commands',
    'setup_utility_commands',
    'setup_help',
    'setup_poll_commands',
    'setup_ticket_commands',
    'setup_giveaway_commands',
    'setup_reminder_commands',
    'setup_custom_commands',
    'setup_leveling_system',
]
