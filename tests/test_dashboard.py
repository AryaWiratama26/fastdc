"""
Unit tests for the FastDC Dashboard Quart App
"""

import pytest
import json
from quart import Quart
from unittest.mock import MagicMock, AsyncMock

from fastdc import FastBot
from fastdc.dashboard.server import create_dashboard_app
from fastdc.models import AutoReplyRule


class MockStorage:
    def __init__(self):
        self._data = {}
    
    def get_custom_commands(self): return {}
    def get_xp_data(self): return {}
    def get_auto_replies(self): return []
    def get_settings(self): return {}
    
    def save_custom_commands(self, data): self._data['custom_commands'] = data
    def save_auto_replies(self, data): self._data['auto_replies'] = data
    def save_xp_data(self, data): self._data['xp_data'] = data
    def save_settings(self, data): self._data['settings'] = data


@pytest.fixture
def mock_bot():
    bot = MagicMock(spec=FastBot)
    bot.bot = MagicMock()
    bot.bot.user = MagicMock()
    bot.bot.user.__str__.return_value = "TestBot#1234"
    bot.bot.user.avatar = None
    bot.bot.guilds = []
    bot.bot.latency = 0.05
    bot.bot.command_prefix = "!"
    
    bot.ai_providers = {}
    bot._active_ai_provider = None
    bot._ai_context_file = None
    
    bot._has_anti_spam = False
    bot.anti_spam_config = MagicMock()
    bot.anti_spam_config.max_messages = 5
    bot.anti_spam_config.interval_seconds = 5
    bot.anti_spam_config.action = "warn"
    
    bot._has_leveling = False
    bot._xp_per_message = 15
    
    bot._welcome_enabled = False
    bot._welcome_message = "Hello"
    bot._leave_enabled = False
    bot._leave_message = "Bye"
    bot._auto_role_id = None
    bot._afk_enabled = False
    bot._starboard_enabled = False
    bot._starboard_config = {'channel_id': None, 'emoji': '⭐', 'threshold': 3}
    bot._temp_voice_enabled = False
    bot._temp_voice_config = {'trigger_channel_id': None, 'category_id': None}
    
    bot._presence_status = "online"
    bot._presence_activity_type = "playing"
    bot._presence_activity_name = "FastDC"
    
    bot.auto_replies = []
    bot._custom_commands = {}
    bot._xp_data = {}
    
    bot.storage = MockStorage()
    bot.save_state = MagicMock()
    
    return bot


@pytest.fixture
def app(mock_bot):
    app = create_dashboard_app(mock_bot, password="password123")
    app.config['TESTING'] = True
    return app


@pytest.fixture
def test_client(app):
    return app.test_client()


@pytest.mark.asyncio
async def test_auth_flow(test_client):
    """Test login, accessing protected route, and logout."""
    # 1. Unauthenticated access should redirect to login
    response = await test_client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers.get('Location')

    # 2. Incorrect login
    response = await test_client.post('/login', form={'password': 'wrongpassword'})
    assert response.status_code == 200
    html = await response.get_data(as_text=True)
    assert 'Invalid password' in html

    # 3. Correct login
    response = await test_client.post('/login', form={'password': 'password123'})
    assert response.status_code == 302
    assert response.headers.get('Location') == '/'

    # 4. Authenticated access
    response = await test_client.get('/')
    assert response.status_code == 200

    # 5. Logout
    response = await test_client.get('/logout')
    assert response.status_code == 302
    assert '/login' in response.headers.get('Location')


@pytest.mark.asyncio
async def test_api_status(test_client):
    """Test the /api/status endpoint."""
    # Need to login first
    await test_client.post('/login', form={'password': 'password123'})

    response = await test_client.get('/api/status')
    assert response.status_code == 200
    data = await response.get_json()
    assert data['online'] is True
    assert data['name'] == 'TestBot#1234'
    assert data['prefix'] == '!'
    assert data['latency'] == 50.0


@pytest.mark.asyncio
async def test_api_settings_get(test_client):
    """Test fetching settings."""
    await test_client.post('/login', form={'password': 'password123'})

    response = await test_client.get('/api/settings')
    assert response.status_code == 200
    data = await response.get_json()
    
    assert data['prefix'] == '!'
    assert 'anti_spam' in data
    assert data['anti_spam']['max_messages'] == 5
    assert data['leveling']['xp_per_message'] == 15
    assert data['welcome']['message'] == 'Hello'
    assert data['presence']['status'] == 'online'


@pytest.mark.asyncio
async def test_api_settings_post(test_client, mock_bot):
    """Test updating settings."""
    await test_client.post('/login', form={'password': 'password123'})

    payload = {
        'prefix': '?',
        'anti_spam': {'max_messages': 10, 'interval': 2, 'action': 'mute'},
        'leveling': {'xp_per_message': 50},
        'welcome': {'message': 'Welcome test!'},
        'auto_role': {'role_id': '123456789'},
    }

    response = await test_client.post('/api/settings', json=payload)
    assert response.status_code == 200
    assert (await response.get_json())['status'] == 'ok'

    # Verify bot instance was updated
    assert mock_bot.bot.command_prefix == '?'
    assert mock_bot.anti_spam_config.max_messages == 10
    assert mock_bot.anti_spam_config.action == 'mute'
    assert mock_bot._xp_per_message == 50
    assert mock_bot._welcome_message == 'Welcome test!'
    assert mock_bot._auto_role_id == 123456789  # int cast


@pytest.mark.asyncio
async def test_api_custom_commands(test_client, mock_bot):
    """Test CRUD operations for custom commands."""
    await test_client.post('/login', form={'password': 'password123'})

    # 1. Add command
    response = await test_client.post('/api/commands', json={'name': 'ping', 'response': 'pong!'})
    assert response.status_code == 200
    assert mock_bot._custom_commands['ping'] == 'pong!'

    # 2. Get commands
    response = await test_client.get('/api/commands')
    data = await response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'ping'
    assert data[0]['response'] == 'pong!'

    # 3. Delete command
    response = await test_client.delete('/api/commands/ping')
    assert response.status_code == 200
    assert 'ping' not in mock_bot._custom_commands


@pytest.mark.asyncio
async def test_api_autoreplies(test_client, mock_bot):
    """Test CRUD operations for auto replies."""
    await test_client.post('/login', form={'password': 'password123'})

    # 1. Add auto reply
    response = await test_client.post('/api/autoreplies', json={'trigger': 'hello', 'response': 'hi there'})
    assert response.status_code == 200
    assert len(mock_bot.auto_replies) == 1
    assert mock_bot.auto_replies[0].trigger == 'hello'
    assert mock_bot.auto_replies[0].response == 'hi there'

    # 2. Delete auto reply
    response = await test_client.delete('/api/autoreplies/0')
    assert response.status_code == 200
    assert len(mock_bot.auto_replies) == 0


@pytest.mark.asyncio
async def test_api_save(test_client, mock_bot):
    """Test manual save endpoint."""
    await test_client.post('/login', form={'password': 'password123'})

    response = await test_client.post('/api/save')
    assert response.status_code == 200
    mock_bot.save_state.assert_called_once()
