"""
FastDC — A Fast Discord Bot Framework
"""

import logging
from typing import List

import discord
from discord.ext import commands

from .models import AIProvider, AutoReplyRule, ReactionRoleMapping, AntiSpamConfig
from .exceptions import FastDCError, ProviderNotConfigured, InvalidProvider
from .utils.embed_builder import QuickEmbed
from .utils.scheduler import MessageScheduler
from .utils.paginator import EmbedPaginator
from .utils.storage import JSONStorage

from .commands.ai import setup_ai_commands
from .commands.moderation import setup_moderation_commands
from .commands.utility import setup_utility_commands, setup_help
from .commands.poll import setup_poll_commands
from .commands.ticket import setup_ticket_commands
from .commands.giveaway import setup_giveaway_commands
from .commands.reminder import setup_reminder_commands
from .commands.custom_commands import setup_custom_commands
from .commands.leveling import setup_leveling_system

from .events.logging import setup_event_logging
from .events.welcome import setup_welcome, setup_leave
from .events.auto_reply import setup_auto_reply
from .events.reaction_roles import setup_reaction_roles
from .events.anti_spam import setup_anti_spam
from .events.auto_role import setup_auto_role
from .events.afk import setup_afk_system
from .events.starboard import setup_starboard
from .events.temp_voice import setup_temp_voice
from .events.button_roles import setup_button_roles


class FastBot:
    """
    Main FastDC Bot class — orchestrates all features.

    Usage:
        bot = FastBot(token="YOUR_TOKEN")
        bot.add_ai_provider("groq", "API_KEY")
        bot.ai_chat(provider="groq")
        bot.run()
    """

    def __init__(self, token: str, prefix: str = "!", data_file: str = "fastdc_data.json"):
        self.token = token
        self.bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
        self.ai_providers = {}
        self.auto_replies: List[AutoReplyRule] = []
        self.reaction_roles: List[ReactionRoleMapping] = []
        self.anti_spam_config = AntiSpamConfig()
        self.scheduler = None
        self.logger = logging.getLogger('fastdc')
        self._has_anti_spam = False
        self._has_leveling = False
        self._button_role_configs = []
        self._dashboard_app = None
        self._dashboard_port = 5000
        self._dashboard_port = 5000
        self.storage = JSONStorage(data_file)

        self._welcome_enabled = False
        self._welcome_message = "Hello {member}, welcome to Server!"
        self._leave_enabled = False
        self._leave_message = "{member} has left the server"
        self._auto_role_id = None
        self._afk_enabled = False
        self._starboard_enabled = False
        self._starboard_config = {'channel_id': None, 'emoji': '⭐', 'threshold': 3}
        self._temp_voice_enabled = False
        self._temp_voice_config = {'trigger_channel_id': None, 'category_id': None}
        self._reaction_roles_enabled = False
        self._button_roles_enabled = False

        self._load_persisted_data()
        self._setup_logging()

    def _load_persisted_data(self):
        """Load saved data from JSON storage."""
        self._custom_commands = self.storage.get_custom_commands()
        self._xp_data = self.storage.get_xp_data()

        saved_replies = self.storage.get_auto_replies()
        for r in saved_replies:
            self.auto_replies.append(AutoReplyRule(trigger=r['trigger'], response=r['response']))

        saved = self.storage.get_settings()
        if 'prefix' in saved:
            self.bot.command_prefix = saved['prefix']
        if 'anti_spam' in saved:
            cfg = saved['anti_spam']
            self.anti_spam_config.max_messages = cfg.get('max_messages', 5)
            self.anti_spam_config.interval_seconds = cfg.get('interval', 5)
            self.anti_spam_config.action = cfg.get('action', 'mute')
        if 'xp_per_message' in saved:
            self._xp_per_message = saved['xp_per_message']
        if 'presence' in saved:
            p = saved['presence']
            self._presence_status = p.get('status', 'online')
            self._presence_activity_type = p.get('activity_type', 'playing')
            self._presence_activity_name = p.get('activity_name', 'FastDC Bot')

    def save_state(self):
        """Save current state to JSON storage. Called by dashboard API."""
        self.storage.save_custom_commands(self._custom_commands if hasattr(self, '_custom_commands') else {})
        self.storage.save_auto_replies(self.auto_replies)
        if hasattr(self, '_xp_data'):
            self.storage.save_xp_data(self._xp_data)

    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def add_ai_provider(self, provider: str, api_key: str, model: str = None):
        """
        Add and cache an AI provider client.

        Parameters:
        ----------
        provider : str — 'groq' or 'openai'
        api_key : str — API key
        model : str, optional — Model name
        """
        client = None
        if provider == 'groq':
            from groq import Groq
            client = Groq(api_key=api_key)
        elif provider == 'openai':
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
        else:
            raise InvalidProvider(provider)

        self.ai_providers[provider] = AIProvider(
            name=provider, api_key=api_key, model=model, client=client
        )

    def ai_chat(self, provider: str = 'groq', context_file: str = None):
        """Enable AI chat commands (!ai and /ai)."""
        if provider not in self.ai_providers:
            raise ProviderNotConfigured(provider)
        self._active_ai_provider = provider
        self._ai_context_file = context_file
        setup_ai_commands(self, provider, context_file)

    def setup_command_categories(self):
        """Register the help command system"""
        setup_help(self)

    def add_moderation_commands(self):
        """Add kick, ban, clear (prefix + slash)"""
        setup_moderation_commands(self)

    def add_utility_commands(self):
        """Add ping, serverinfo (prefix + slash)"""
        setup_utility_commands(self)

    def add_poll_commands(self):
        """Add poll system (prefix + slash)"""
        setup_poll_commands(self)

    def add_ticket_system(self):
        """Add ticket system (prefix + slash)"""
        setup_ticket_commands(self)

    def add_giveaway_commands(self):
        """Add giveaway system (prefix + slash)"""
        setup_giveaway_commands(self)

    def add_reminder_commands(self):
        """Add reminder system (prefix + slash)"""
        setup_reminder_commands(self)

    def add_custom_commands(self):
        """Add custom command system (!addcmd, !delcmd, !listcmds)"""
        setup_custom_commands(self)

    def enable_leveling(self, xp_per_message: int = 15):
        """
        Enable XP/leveling system.

        Parameters:
        ----------
        xp_per_message : int — Max XP gain per message (default: 15)
        """
        self._has_leveling = True
        self._xp_per_message = xp_per_message
        setup_leveling_system(self)

    def setup_event_logging(self):
        """Enable command and error logging"""
        setup_event_logging(self)

    def auto_reply(self, trigger: str, response: str):
        """Add an auto-reply rule. Supports multiple triggers."""
        self.auto_replies.append(AutoReplyRule(trigger=trigger.lower(), response=response))

    def welcome_member(self, message: str = "Hello {member}, welcome to Server!"):
        """Send welcome message on member join. Use {member} as placeholder."""
        setup_welcome(self, message)

    def leave_member(self, message: str = "{member} has left the server"):
        """Send leave message on member leave. Use {member} as placeholder."""
        setup_leave(self, message)

    def add_reaction_role(self, message_id: int, emoji: str, role_id: int):
        """Map a reaction on a message to a role."""
        self.reaction_roles.append(ReactionRoleMapping(
            message_id=message_id, emoji=emoji, role_id=role_id
        ))

    def enable_reaction_roles(self):
        """Activate the reaction role system"""
        setup_reaction_roles(self)

    def enable_anti_spam(self, max_messages: int = 5, interval: int = 5, action: str = "mute", mute_duration: int = 300):
        """
        Enable anti-spam detection.

        Parameters:
        ----------
        max_messages : int — Max messages in interval (default: 5)
        interval : int — Time window in seconds (default: 5)
        action : str — 'mute', 'kick', or 'warn' (default: 'mute')
        mute_duration : int — Mute seconds if action is 'mute' (default: 300)
        """
        self.anti_spam_config = AntiSpamConfig(
            max_messages=max_messages,
            interval_seconds=interval,
            action=action,
            mute_duration=mute_duration
        )
        self._has_anti_spam = True

    def auto_role(self, role_id: int):
        """Auto-assign a role when members join."""
        setup_auto_role(self, role_id)

    def enable_afk_system(self):
        """Enable AFK system (!afk, auto-notify on mention)"""
        setup_afk_system(self)

    def enable_starboard(self, channel_id: int, emoji: str = "⭐", threshold: int = 3):
        """
        Enable starboard — popular messages reposted to a channel.

        Parameters:
        ----------
        channel_id : int — Starboard channel ID
        emoji : str — Emoji to track (default: ⭐)
        threshold : int — Min reactions to post (default: 3)
        """
        setup_starboard(self, channel_id, emoji, threshold)

    def enable_temp_voice(self, trigger_channel_id: int, category_id: int = None):
        """
        Enable temp voice channels.

        Parameters:
        ----------
        trigger_channel_id : int — ID of "Join to Create" voice channel
        category_id : int, optional — Category for temp channels
        """
        setup_temp_voice(self, trigger_channel_id, category_id)

    def add_button_role(self, role_id: int, label: str, emoji: str = None, style: str = "primary"):
        """
        Configure a button for the role picker panel.

        Parameters:
        ----------
        role_id : int — Role ID to assign
        label : str — Button label
        emoji : str, optional — Button emoji
        style : str — 'primary', 'secondary', 'success', 'danger'
        """
        self._button_role_configs.append({
            'role_id': role_id, 'label': label, 'emoji': emoji, 'style': style
        })

    def enable_button_roles(self):
        """Activate button/dropdown role picker commands (!rolepanel, /rolepanel)"""
        setup_button_roles(self)

    def set_presence(self, status: str = "online", activity_type: str = "playing", activity_name: str = "FastDC Bot"):
        """Set bot presence. status: online/idle/dnd/invisible. activity_type: playing/watching/listening."""
        self._presence_status = status
        self._presence_activity_type = activity_type
        self._presence_activity_name = activity_name

    def schedule_message(self, channel_id: int, message: str, delay_seconds: float):
        """Schedule a message to be sent after a delay (only works after bot.run())."""
        if self.scheduler is None:
            self.scheduler = MessageScheduler(self.bot)
        self.scheduler.schedule(channel_id, message, delay_seconds)

    @staticmethod
    def quick_embed(title, description="", color=None, **kwargs):
        """Quick helper to create Discord embeds."""
        return QuickEmbed.build(title=title, description=description, color=color, **kwargs)

    @staticmethod
    def paginate(pages: list):
        """Create an EmbedPaginator view for multi-page embeds."""
        return EmbedPaginator(pages)

    def enable_dashboard(self, port: int = 5000, password: str = "admin"):
        """
        Enable web dashboard at http://localhost:{port}.

        Parameters:
        ----------
        port : int — Port number (default: 5000)
        password : str — Login password (default: 'admin')
        """
        from .dashboard import create_dashboard_app
        self._dashboard_app = create_dashboard_app(self, password)
        self._dashboard_port = port
        self.logger.info(f"Dashboard will start at http://localhost:{port}")

    async def sync_commands(self, guild: discord.Guild = None):
        """Sync slash commands with Discord."""
        if guild:
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild)
            self.logger.info(f"Slash commands synced to {guild.name}")
        else:
            await self.bot.tree.sync()
            self.logger.info("Slash commands synced globally")

    def run(self, message_run: str = "{bot} Ready to Use!"):
        """Start the Discord bot."""
        import asyncio

        # Setup on_message handler (anti-spam includes all integrations)
        if self._has_anti_spam or self.auto_replies or self._has_leveling or hasattr(self, '_custom_commands') or hasattr(self, '_afk_users'):
            setup_anti_spam(self)
        elif self.auto_replies:
            setup_auto_reply(self)

        @self.bot.event
        async def on_ready():
            self.scheduler = MessageScheduler(self.bot)

            # Background auto-save loop
            async def _auto_save_loop():
                while True:
                    await asyncio.sleep(300) 
                    self.save_state()
            self.bot.loop.create_task(_auto_save_loop())

            # Set presence
            if hasattr(self, '_presence_activity_type'):
                activity_types = {
                    'playing': discord.ActivityType.playing,
                    'watching': discord.ActivityType.watching,
                    'listening': discord.ActivityType.listening,
                    'streaming': discord.ActivityType.streaming,
                }
                status_types = {
                    'online': discord.Status.online,
                    'idle': discord.Status.idle,
                    'dnd': discord.Status.dnd,
                    'invisible': discord.Status.invisible,
                }
                activity = discord.Activity(
                    type=activity_types.get(self._presence_activity_type, discord.ActivityType.playing),
                    name=self._presence_activity_name
                )
                status = status_types.get(self._presence_status, discord.Status.online)
                await self.bot.change_presence(activity=activity, status=status)

            await self.sync_commands()

            bot_name = str(self.bot.user)
            if "{bot}" in message_run:
                print(message_run.replace("{bot}", bot_name))
            else:
                print(f"{bot_name} Ready to Use!")

            # Log dashboard URL if enabled
            if self._dashboard_app:
                self.logger.info(f"Dashboard running at http://localhost:{self._dashboard_port}")

        # Run with or without dashboard
        if self._dashboard_app:
            async def _start():
                from hypercorn.asyncio import serve
                from hypercorn.config import Config

                hconfig = Config()
                hconfig.bind = [f"0.0.0.0:{self._dashboard_port}"]
                hconfig.accesslog = None
                hconfig.errorlog = None

                # Run both bot and dashboard concurrently
                await asyncio.gather(
                    self.bot.start(self.token),
                    serve(self._dashboard_app, hconfig)
                )

            asyncio.run(_start())
        else:
            self.bot.run(self.token)
