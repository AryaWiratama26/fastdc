"""
FastDC Dashboard Server
Provides a Quart web server and REST API for managing bot settings and features.
"""

import os
import logging
import secrets
from datetime import datetime

from quart import Quart, render_template, request, session, redirect, url_for, jsonify
from .auth import login_required

logger = logging.getLogger('fastdc.dashboard')

def safe_int(val, default=None):
    """Safely convert value to int, returning default on failure."""
    if not val or str(val).lower() == 'none':
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def create_dashboard_app(bot_instance, password: str = "admin"):
    """Create a Quart web application for the bot dashboard."""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'static')

    app = Quart(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = secrets.token_hex(32)

    log_entries = []
    MAX_LOGS = 100

    def add_log(action: str, detail: str = ""):
        """Add an entry to the in-memory dashboard activity log."""
        log_entries.insert(0, {
            'time': datetime.now().strftime('%H:%M:%S'),
            'action': action,
            'detail': detail
        })
        if len(log_entries) > MAX_LOGS:
            log_entries.pop()

    bot_instance._dashboard_logs = log_entries
    bot_instance._add_dashboard_log = add_log

    @app.route('/login', methods=['GET', 'POST'])
    async def login():
        """Handle dashboard authentication."""
        error = None
        if request.method == 'POST':
            form = await request.form
            if form.get('password') == password:
                session['authenticated'] = True
                add_log("Login", "Dashboard accessed")
                return redirect(url_for('dashboard'))
            error = "Invalid password"
        return await render_template('login.html', error=error)

    @app.route('/logout')
    async def logout():
        """Clear the current session and logout."""
        session.clear()
        return redirect(url_for('login'))

    @app.route('/')
    @login_required
    async def dashboard():
        """Render the main dashboard interface."""
        return await render_template('dashboard.html')

    @app.route('/api/status')
    @login_required
    async def api_status():
        """Return the current bot health, statistics, and latency."""
        bot = bot_instance.bot
        if bot.user:
            return jsonify({
                'online': True,
                'name': str(bot.user),
                'avatar': str(bot.user.avatar.url) if bot.user.avatar else None,
                'guilds': len(bot.guilds),
                'members': sum(g.member_count or 0 for g in bot.guilds),
                'latency': round(bot.latency * 1000, 1),
                'prefix': bot.command_prefix,
            })
        return jsonify({'online': False})

    @app.route('/api/settings')
    @login_required
    async def api_settings():
        """Retrieve all configurable bot settings and their current values."""
        # AI info
        ai_info = {}
        for name, provider in bot_instance.ai_providers.items():
            ai_info[name] = {
                'model': provider.model or 'default',
                'active': name == getattr(bot_instance, '_active_ai_provider', None),
            }

        return jsonify({
            'ai': {
                'providers': ai_info,
                'active_provider': getattr(bot_instance, '_active_ai_provider', None),
                'context_file': getattr(bot_instance, '_ai_context_file', None),
            },
            'anti_spam': {
                'enabled': bot_instance._has_anti_spam,
                'max_messages': bot_instance.anti_spam_config.max_messages,
                'interval': bot_instance.anti_spam_config.interval_seconds,
                'action': bot_instance.anti_spam_config.action,
            },
            'leveling': {
                'enabled': bot_instance._has_leveling,
                'xp_per_message': getattr(bot_instance, '_xp_per_message', 15),
            },
            'welcome': {
                'enabled': bot_instance._welcome_enabled,
                'message': bot_instance._welcome_message,
            },
            'leave': {
                'enabled': bot_instance._leave_enabled,
                'message': bot_instance._leave_message,
            },
            'auto_role': {
                'enabled': bot_instance._auto_role_id is not None,
                'role_id': bot_instance._auto_role_id,
            },
            'afk': {
                'enabled': bot_instance._afk_enabled,
            },
            'starboard': {
                'enabled': bot_instance._starboard_enabled,
                **bot_instance._starboard_config,
            },
            'temp_voice': {
                'enabled': bot_instance._temp_voice_enabled,
                **bot_instance._temp_voice_config,
            },
            'presence': {
                'status': getattr(bot_instance, '_presence_status', 'online'),
                'activity_type': getattr(bot_instance, '_presence_activity_type', 'playing'),
                'activity_name': getattr(bot_instance, '_presence_activity_name', 'FastDC Bot'),
            },
            'auto_replies': [
                {'trigger': r.trigger, 'response': r.response}
                for r in bot_instance.auto_replies
            ],
            'prefix': bot_instance.bot.command_prefix,
        })

    @app.route('/api/settings', methods=['POST'])
    @login_required
    async def api_update_settings():
        """Update bot settings based on JSON payload and persist to storage."""
        data = await request.get_json()

        if 'prefix' in data:
            bot_instance.bot.command_prefix = data['prefix']
            bot_instance.storage.save_settings({'prefix': data['prefix']})
            add_log("Settings", f"Prefix changed to {data['prefix']}")

        if 'ai' in data:
            cfg = data['ai']
            if 'active_provider' in cfg and cfg['active_provider'] in bot_instance.ai_providers:
                bot_instance._active_ai_provider = cfg['active_provider']
                add_log("AI", f"Provider: {cfg['active_provider']}")
            if 'model' in cfg:
                pname = getattr(bot_instance, '_active_ai_provider', None)
                if pname and pname in bot_instance.ai_providers:
                    bot_instance.ai_providers[pname].model = cfg['model']
                    add_log("AI", f"Model: {cfg['model']}")
            if 'context_file' in cfg:
                bot_instance._ai_context_file = cfg['context_file'] or None
                add_log("AI", f"Context: {cfg['context_file'] or 'none'}")

        if 'anti_spam' in data:
            cfg = data['anti_spam']
            bot_instance.anti_spam_config.max_messages = safe_int(cfg.get('max_messages'), 5)
            bot_instance.anti_spam_config.interval_seconds = safe_int(cfg.get('interval'), 5)
            bot_instance.anti_spam_config.action = cfg.get('action', 'warn')
            bot_instance.storage.save_settings({'anti_spam': {
                'max_messages': bot_instance.anti_spam_config.max_messages,
                'interval': bot_instance.anti_spam_config.interval_seconds,
                'action': bot_instance.anti_spam_config.action,
            }})
            add_log("Settings", f"Anti-spam: {cfg.get('action')}")

        if 'leveling' in data:
            bot_instance._xp_per_message = safe_int(data['leveling'].get('xp_per_message'), 15)
            bot_instance.storage.save_settings({'xp_per_message': bot_instance._xp_per_message})
            add_log("Settings", f"XP/msg: {bot_instance._xp_per_message}")

        if 'welcome' in data:
            cfg = data['welcome']
            if 'message' in cfg:
                bot_instance._welcome_message = cfg['message']
                add_log("Settings", "Welcome message updated")

        if 'leave' in data:
            cfg = data['leave']
            if 'message' in cfg:
                bot_instance._leave_message = cfg['message']
                add_log("Settings", "Leave message updated")

        if 'auto_role' in data:
            role_id = safe_int(data['auto_role'].get('role_id'))
            bot_instance._auto_role_id = role_id
            add_log("Settings", f"Auto role: {role_id or 'disabled'}")

        if 'starboard' in data:
            cfg = data['starboard']
            if 'channel_id' in cfg:
                bot_instance._starboard_config['channel_id'] = safe_int(cfg['channel_id'])
            if 'emoji' in cfg:
                bot_instance._starboard_config['emoji'] = cfg['emoji'] or '⭐'
            if 'threshold' in cfg:
                bot_instance._starboard_config['threshold'] = safe_int(cfg.get('threshold'), 3)
            add_log("Settings", "Starboard updated")

        if 'temp_voice' in data:
            cfg = data['temp_voice']
            if 'trigger_channel_id' in cfg:
                bot_instance._temp_voice_config['trigger_channel_id'] = safe_int(cfg['trigger_channel_id'])
            add_log("Settings", "Temp voice updated")

        if 'presence' in data:
            import discord
            cfg = data['presence']
            bot_instance._presence_status = cfg.get('status', 'online')
            bot_instance._presence_activity_type = cfg.get('activity_type', 'playing')
            bot_instance._presence_activity_name = cfg.get('activity_name', 'FastDC Bot')
            bot_instance.storage.save_settings({'presence': {
                'status': bot_instance._presence_status,
                'activity_type': bot_instance._presence_activity_type,
                'activity_name': bot_instance._presence_activity_name,
            }})

            # Apply presence change live
            activity_types = {
                'playing': discord.ActivityType.playing,
                'watching': discord.ActivityType.watching,
                'listening': discord.ActivityType.listening,
            }
            status_types = {
                'online': discord.Status.online,
                'idle': discord.Status.idle,
                'dnd': discord.Status.dnd,
                'invisible': discord.Status.invisible,
            }
            try:
                activity = discord.Activity(
                    type=activity_types.get(bot_instance._presence_activity_type, discord.ActivityType.playing),
                    name=bot_instance._presence_activity_name
                )
                status = status_types.get(bot_instance._presence_status, discord.Status.online)
                import asyncio
                asyncio.ensure_future(bot_instance.bot.change_presence(activity=activity, status=status))
                add_log("Presence", f"{cfg.get('activity_type')} {cfg.get('activity_name')}")
            except Exception:
                pass

        return jsonify({'status': 'ok'})

    @app.route('/api/commands')
    @login_required
    async def api_commands():
        """Retrieve a list of all custom commands."""
        cmds = getattr(bot_instance, '_custom_commands', {})
        return jsonify([{'name': n, 'response': r} for n, r in cmds.items()])

    @app.route('/api/commands', methods=['POST'])
    @login_required
    async def api_add_command():
        """Create a new custom command."""
        data = await request.get_json()
        name = data.get('name', '').lower().strip()
        response = data.get('response', '').strip()
        if not name or not response:
            return jsonify({'error': 'Name and response required'}), 400

        if not hasattr(bot_instance, '_custom_commands'):
            bot_instance._custom_commands = {}
        bot_instance._custom_commands[name] = response
        bot_instance.storage.save_custom_commands(bot_instance._custom_commands)
        add_log("Command", f"Added !{name}")
        return jsonify({'status': 'ok'})

    @app.route('/api/commands/<name>', methods=['DELETE'])
    @login_required
    async def api_delete_command(name):
        """Delete an existing custom command by name."""
        cmds = getattr(bot_instance, '_custom_commands', {})
        if name in cmds:
            del cmds[name]
            bot_instance.storage.save_custom_commands(cmds)
            add_log("Command", f"Deleted !{name}")
            return jsonify({'status': 'ok'})
        return jsonify({'error': 'Not found'}), 404

    @app.route('/api/autoreplies', methods=['POST'])
    @login_required
    async def api_add_autoreply():
        """Add a new auto-reply rule."""
        data = await request.get_json()
        trigger = data.get('trigger', '').lower().strip()
        response = data.get('response', '').strip()
        if not trigger or not response:
            return jsonify({'error': 'Required'}), 400

        from ..models import AutoReplyRule
        bot_instance.auto_replies.append(AutoReplyRule(trigger=trigger, response=response))
        bot_instance.storage.save_auto_replies(bot_instance.auto_replies)
        add_log("Auto-Reply", f"Added: {trigger}")
        return jsonify({'status': 'ok'})

    @app.route('/api/autoreplies/<int:index>', methods=['DELETE'])
    @login_required
    async def api_delete_autoreply(index):
        """Delete an auto-reply rule by its index."""
        if 0 <= index < len(bot_instance.auto_replies):
            removed = bot_instance.auto_replies.pop(index)
            bot_instance.storage.save_auto_replies(bot_instance.auto_replies)
            add_log("Auto-Reply", f"Removed: {removed.trigger}")
            return jsonify({'status': 'ok'})
        return jsonify({'error': 'Not found'}), 404

    @app.route('/api/leaderboard')
    @login_required
    async def api_leaderboard():
        """Fetch the top 10 users by XP across all servers."""
        xp_data = getattr(bot_instance, '_xp_data', {})
        result = []
        for guild in bot_instance.bot.guilds:
            guild_xp = xp_data.get(guild.id, {})
            sorted_users = sorted(guild_xp.items(), key=lambda x: x[1], reverse=True)[:10]
            for user_id, xp in sorted_users:
                member = guild.get_member(user_id)
                from ..commands.leveling import level_from_xp
                result.append({
                    'name': member.display_name if member else f'User {user_id}',
                    'xp': xp,
                    'level': level_from_xp(xp),
                    'guild': guild.name,
                })
        return jsonify(result)

    @app.route('/api/logs')
    @login_required
    async def api_logs():
        """Fetch the 50 most recent dashboard activity logs."""
        return jsonify(log_entries[:50])

    @app.route('/api/save', methods=['POST'])
    @login_required
    async def api_save():
        """Manually trigger a save of all bot state to persistent storage."""
        bot_instance.save_state()
        add_log("System", "Data saved to disk")
        return jsonify({'status': 'ok'})

    return app
