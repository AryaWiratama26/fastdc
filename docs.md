# FastDC Documentation

Full API reference for FastDC v2.2.0.

---

## Table of Contents

- [FastBot](#fastbot)
  - [Initialization](#initialization)
  - [AI Integration](#ai-integration)
  - [Command Registration](#command-registration)
  - [Event Configuration](#event-configuration)
  - [Role Management](#role-management)
  - [Presence and Scheduling](#presence-and-scheduling)
  - [Embed Utilities](#embed-utilities)
  - [Dashboard](#dashboard)
  - [Running the Bot](#running-the-bot)
- [QuickEmbed](#quickembed)
- [EmbedPaginator](#embedpaginator)
- [Data Models](#data-models)
- [Exceptions](#exceptions)
- [Data Persistence](#data-persistence)

---

## FastBot

The main class that orchestrates all bot features. Import from the `fastdc` package:

```python
from fastdc import FastBot
```

### Initialization

```python
FastBot(token: str, prefix: str = "!", data_file: str = "fastdc_data.json")
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `token` | str | (required) | Discord bot token |
| `prefix` | str | `"!"` | Command prefix for prefix-based commands |
| `data_file` | str | `"fastdc_data.json"` | Filepath for JSON data persistence |

Example:

```python
bot = FastBot(token="YOUR_TOKEN", prefix="?")
```

---

### AI Integration

#### add_ai_provider

```python
bot.add_ai_provider(provider: str, api_key: str, model: str = None)
```

Register an AI provider client. Must be called before `ai_chat()`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `provider` | str | (required) | Provider name: `"groq"` or `"openai"` |
| `api_key` | str | (required) | API key for the provider |
| `model` | str | `None` | Model name (uses provider default if not set) |

Raises `InvalidProvider` if the provider name is not `"groq"` or `"openai"`.

Example:

```python
bot.add_ai_provider("groq", "gsk_xxxxxxxxxxxx")
bot.add_ai_provider("openai", "sk-xxxxxxxxxxxx", model="gpt-4")
```

#### ai_chat

```python
bot.ai_chat(provider: str = "groq", context_file: str = None)
```

Enable AI chat commands (`!ai` and `/ai`).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `provider` | str | `"groq"` | Which registered provider to use |
| `context_file` | str | `None` | Path to a text file for context-aware responses |

Raises `ProviderNotConfigured` if the provider has not been added via `add_ai_provider()`.

The context file should contain entries separated by double newlines. The bot uses fuzzy matching to find relevant context for each user query.

Example:

```python
bot.add_ai_provider("groq", "API_KEY")
bot.ai_chat(provider="groq", context_file="knowledge.txt")
```

---

### Command Registration

All command methods register both prefix and slash command variants.

#### setup_command_categories

```python
bot.setup_command_categories()
```

Register the help command system (`!bothelp` and `/help`). Call this before other commands if you want help to appear.

#### add_moderation_commands

```python
bot.add_moderation_commands()
```

Registers `!kick` / `/kick`, `!ban` / `/ban`, `!clear` / `/clear`. Requires appropriate Discord permissions (`kick_members`, `ban_members`, `manage_messages`).

#### add_utility_commands

```python
bot.add_utility_commands()
```

Registers `!ping` / `/ping` and `!serverinfo` / `/serverinfo`.

#### add_poll_commands

```python
bot.add_poll_commands()
```

Registers `!poll` / `/poll`. The prefix command supports a question with up to 10 options. The slash command supports up to 5 options. Options are voted on using numbered emoji reactions.

Usage:

```
!poll "What is your favorite color?" "Red" "Blue" "Green"
```

#### add_ticket_system

```python
bot.add_ticket_system()
```

Registers `!ticket` / `/ticket` and `!close` / `/close`. Creates private channels prefixed with `ticket-` under a "Tickets" category.

#### add_giveaway_commands

```python
bot.add_giveaway_commands()
```

Registers `!giveaway` / `/giveaway`. Parses duration strings with units:

| Unit | Example | Seconds |
|---|---|---|
| `s` | `30s` | 30 |
| `m` | `5m` | 300 |
| `h` | `1h` | 3600 |
| `d` | `2d` | 172800 |

Users enter by reacting with the party emoji. A random winner is selected when the timer expires.

Usage:

```
!giveaway 1h "Discord Nitro"
```

#### add_reminder_commands

```python
bot.add_reminder_commands()
```

Registers `!remind` / `/remind`. Uses the same duration format as giveaways. The bot sends a DM when the timer expires, or sends in the channel if DMs are blocked.

Usage:

```
!remind 30m Check the oven
```

#### add_custom_commands

```python
bot.add_custom_commands()
```

Registers `!addcmd` / `/addcmd`, `!delcmd` / `/delcmd`, and `!listcmds`. Requires `manage_guild` permission. Custom commands are persisted to the JSON data file.

Usage:

```
!addcmd hello Hello everyone!
!delcmd hello
!listcmds
```

#### enable_leveling

```python
bot.enable_leveling(xp_per_message: int = 15)
```

Enable the XP and leveling system. Registers `!rank` / `/rank` and `!leaderboard` / `/leaderboard` (aliases: `!lb`, `!top`).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `xp_per_message` | int | `15` | Maximum XP gained per message (actual gain is random between 10 and `xp_per_message + 10`) |

The leveling formula:
- XP required for level N = N^2 * 100
- Level from XP = floor(sqrt(XP / 100))

XP data is persisted to the JSON data file.

---

### Event Configuration

#### setup_event_logging

```python
bot.setup_event_logging()
```

Enable command logging and error handling. Logs all command usage and handles common errors (cooldown, missing permissions, missing arguments, unknown commands).

#### auto_reply

```python
bot.auto_reply(trigger: str, response: str)
```

Add an auto-reply rule. The trigger is automatically lowercased. When a message contains the trigger text, the bot responds with the specified response. Can be called multiple times to add multiple rules.

| Parameter | Type | Description |
|---|---|---|
| `trigger` | str | Text to match (case-insensitive, substring match) |
| `response` | str | Text to respond with |

Example:

```python
bot.auto_reply("hello", "Hi there!")
bot.auto_reply("bye", "Goodbye!")
```

#### welcome_member

```python
bot.welcome_member(message: str = "Hello {member}, welcome to Server!")
```

Send a welcome message when a member joins. Use `{member}` as a placeholder for the member mention.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `message` | str | `"Hello {member}, welcome to Server!"` | Message template |

#### leave_member

```python
bot.leave_member(message: str = "{member} has left the server")
```

Send a message when a member leaves. Use `{member}` as a placeholder for the member name.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `message` | str | `"{member} has left the server"` | Message template |

#### enable_anti_spam

```python
bot.enable_anti_spam(
    max_messages: int = 5,
    interval: int = 5,
    action: str = "mute",
    mute_duration: int = 300
)
```

Enable anti-spam detection on messages.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `max_messages` | int | `5` | Maximum messages allowed within the interval |
| `interval` | int | `5` | Time window in seconds |
| `action` | str | `"mute"` | Action on spam: `"mute"`, `"kick"`, or `"warn"` |
| `mute_duration` | int | `300` | Timeout duration in seconds (only for `"mute"` action) |

#### enable_afk_system

```python
bot.enable_afk_system()
```

Enable the AFK system. Registers `!afk` / `/afk`. When a user sets AFK status, the bot notifies anyone who mentions them. AFK status is removed when the user sends a message.

Usage:

```
!afk Going to lunch
```

#### enable_starboard

```python
bot.enable_starboard(channel_id: int, emoji: str = "⭐", threshold: int = 3)
```

Enable the starboard feature. Messages that receive enough matching reactions are reposted to the specified channel.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `channel_id` | int | (required) | ID of the starboard channel |
| `emoji` | str | `"⭐"` | Emoji to track |
| `threshold` | int | `3` | Minimum reaction count to trigger repost |

#### enable_temp_voice

```python
bot.enable_temp_voice(trigger_channel_id: int, category_id: int = None)
```

Enable temporary voice channels. When a user joins the trigger channel, a personal voice channel is created. The channel is deleted automatically when it becomes empty.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `trigger_channel_id` | int | (required) | ID of the "Join to Create" voice channel |
| `category_id` | int | `None` | Category to create temp channels in (defaults to trigger channel's category) |

#### auto_role

```python
bot.auto_role(role_id: int)
```

Automatically assign a role when new members join the server.

| Parameter | Type | Description |
|---|---|---|
| `role_id` | int | ID of the role to assign |

---

### Role Management

#### add_reaction_role

```python
bot.add_reaction_role(message_id: int, emoji: str, role_id: int)
```

Map a reaction on a specific message to a role. Users who add the reaction get the role; removing the reaction removes the role.

| Parameter | Type | Description |
|---|---|---|
| `message_id` | int | ID of the target message |
| `emoji` | str | Emoji to react with |
| `role_id` | int | ID of the role to assign |

#### enable_reaction_roles

```python
bot.enable_reaction_roles()
```

Activate the reaction role system. Must be called after all `add_reaction_role()` calls.

#### add_button_role

```python
bot.add_button_role(role_id: int, label: str, emoji: str = None, style: str = "primary")
```

Configure a button for the role picker panel. Call this for each role before calling `enable_button_roles()`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `role_id` | int | (required) | ID of the role to assign |
| `label` | str | (required) | Button label text |
| `emoji` | str | `None` | Button emoji |
| `style` | str | `"primary"` | Button style: `"primary"`, `"secondary"`, `"success"`, `"danger"` |

#### enable_button_roles

```python
bot.enable_button_roles()
```

Activate button/dropdown role picker commands (`!rolepanel` / `/rolepanel`). Requires `manage_roles` permission. Supports two panel types: `buttons` (default) and `dropdown`.

Usage:

```
!rolepanel buttons
!rolepanel dropdown
```

Example setup:

```python
bot.add_button_role(role_id=111, label="Gamer", emoji="G")
bot.add_button_role(role_id=222, label="Artist", emoji="A")
bot.enable_button_roles()
```

---

### Presence and Scheduling

#### set_presence

```python
bot.set_presence(
    status: str = "online",
    activity_type: str = "playing",
    activity_name: str = "FastDC Bot"
)
```

Set the bot's presence (status and activity).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `status` | str | `"online"` | Status: `"online"`, `"idle"`, `"dnd"`, `"invisible"` |
| `activity_type` | str | `"playing"` | Activity type: `"playing"`, `"watching"`, `"listening"`, `"streaming"` |
| `activity_name` | str | `"FastDC Bot"` | Activity text |

#### schedule_message

```python
bot.schedule_message(channel_id: int, message: str, delay_seconds: float)
```

Schedule a message to be sent to a channel after a delay. Only works after `bot.run()` is called.

| Parameter | Type | Description |
|---|---|---|
| `channel_id` | int | Target channel ID |
| `message` | str | Message content |
| `delay_seconds` | float | Delay in seconds before sending |

---

### Embed Utilities

#### quick_embed

```python
FastBot.quick_embed(title, description="", color=None, **kwargs)
```

Static method. Creates a `discord.Embed` using `QuickEmbed.build()`. See [QuickEmbed](#quickembed) for full parameter list.

#### paginate

```python
FastBot.paginate(pages: list)
```

Static method. Creates an `EmbedPaginator` view from a list of embeds. See [EmbedPaginator](#embedpaginator) for details.

---

### Dashboard

#### enable_dashboard

```python
bot.enable_dashboard(port: int = 5000, password: str = "admin")
```

Enable the web dashboard. The dashboard runs concurrently with the bot on the specified port using Hypercorn.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `port` | int | `5000` | Port number for the web server |
| `password` | str | `"admin"` | Login password for the dashboard |

The dashboard provides the following routes and API endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/login` | Login page (renders form on GET, authenticates on POST) |
| GET | `/logout` | Clear session and redirect to login |
| GET | `/` | Main dashboard page (requires login) |
| GET | `/api/status` | Bot status, guild count, and latency |
| GET | `/api/settings` | Get all settings (includes auto-reply rules) |
| POST | `/api/settings` | Update settings (prefix, anti-spam, leveling, presence, etc.) |
| GET | `/api/commands` | List custom commands |
| POST | `/api/commands` | Create a custom command |
| DELETE | `/api/commands/<name>` | Delete a custom command |
| POST | `/api/autoreplies` | Create an auto-reply rule |
| DELETE | `/api/autoreplies/<index>` | Delete an auto-reply rule by index |
| GET | `/api/leaderboard` | Top 10 users by XP across all servers |
| GET | `/api/logs` | 50 most recent dashboard activity logs |
| POST | `/api/save` | Manually save all bot data to disk |

Note: Auto-reply rules are returned as part of the `GET /api/settings` response under the `auto_replies` key.

#### sync_commands

```python
await bot.sync_commands(guild: discord.Guild = None)
```

Sync slash commands with Discord. Called automatically on bot startup. Pass a guild to sync only to that guild (faster for testing).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `guild` | discord.Guild | `None` | Specific guild to sync to. If `None`, syncs globally. |

---

### Running the Bot

#### run

```python
bot.run(message_run: str = "{bot} Ready to Use!")
```

Start the Discord bot. If the dashboard is enabled, the bot and dashboard run concurrently.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `message_run` | str | `"{bot} Ready to Use!"` | Startup message. `{bot}` is replaced with the bot's username. |

The `run()` method also:
- Starts a background auto-save loop (every 5 minutes)
- Sets the configured presence
- Syncs slash commands globally
- Sets up the unified `on_message` handler

#### save_state

```python
bot.save_state()
```

Manually save all persisted data (custom commands, auto-replies, XP data). Called automatically every 5 minutes and by the dashboard API.

---

## QuickEmbed

Utility class for creating styled Discord embeds. Import from `fastdc`:

```python
from fastdc import QuickEmbed
```

### Color Constants

| Constant | Color |
|---|---|
| `QuickEmbed.PRIMARY` | Blue |
| `QuickEmbed.SUCCESS` | Green |
| `QuickEmbed.WARNING` | Orange |
| `QuickEmbed.ERROR` | Red |
| `QuickEmbed.INFO` | Blurple |
| `QuickEmbed.PURPLE` | Purple |

### QuickEmbed.build

```python
QuickEmbed.build(
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
) -> discord.Embed
```

Static method. Returns a `discord.Embed` with the specified properties.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | str | (required) | Embed title |
| `description` | str | `""` | Embed description |
| `color` | discord.Color | `PRIMARY` | Embed sidebar color |
| `fields` | list | `None` | List of `(name, value, inline)` tuples |
| `thumbnail` | str | `None` | Thumbnail image URL |
| `image` | str | `None` | Main image URL |
| `footer` | str | `None` | Footer text |
| `author_name` | str | `None` | Author name |
| `author_icon` | str | `None` | Author icon URL |
| `timestamp` | bool | `False` | Add current timestamp |

### Preset Methods

```python
QuickEmbed.success(title: str, description: str = "") -> discord.Embed
QuickEmbed.error(title: str, description: str = "") -> discord.Embed
QuickEmbed.warning(title: str, description: str = "") -> discord.Embed
QuickEmbed.info(title: str, description: str = "") -> discord.Embed
```

Each preset uses the corresponding color and adds a status icon prefix to the title.

---

## EmbedPaginator

A `discord.ui.View` subclass that adds page navigation buttons to multi-page embeds. Import from `fastdc`:

```python
from fastdc import EmbedPaginator
```

### Constructor

```python
EmbedPaginator(pages: List[discord.Embed], timeout: float = 120)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pages` | List[discord.Embed] | (required) | List of `discord.Embed` objects |
| `timeout` | float | `120` | View timeout in seconds |

### Usage

```python
import discord
from fastdc import EmbedPaginator

pages = [
    discord.Embed(title="Page 1", description="Content 1"),
    discord.Embed(title="Page 2", description="Content 2"),
    discord.Embed(title="Page 3", description="Content 3"),
]

paginator = EmbedPaginator(pages)
await ctx.send(embed=pages[0], view=paginator)
```

The view provides five buttons:
- First page
- Previous page
- Page counter (disabled, shows current/total)
- Next page
- Last page

Buttons are automatically disabled at the boundaries (first page disables previous, last page disables next).

---

## Data Models

Dataclasses defined in `fastdc.models`.

### AIProvider

```python
@dataclass
class AIProvider:
    name: str
    api_key: str
    model: str = None
    client: Any = None
```

### AutoReplyRule

```python
@dataclass
class AutoReplyRule:
    trigger: str
    response: str
```

### ReactionRoleMapping

```python
@dataclass
class ReactionRoleMapping:
    message_id: int
    emoji: str
    role_id: int
```

### AntiSpamConfig

```python
@dataclass
class AntiSpamConfig:
    max_messages: int = 5
    interval_seconds: int = 5
    action: str = "mute"
    mute_duration: int = 300
```

### ScheduledMessage

```python
@dataclass
class ScheduledMessage:
    channel_id: int
    message: str
    delay_seconds: float
    task: Any = None
```

---

## Exceptions

Custom exceptions defined in `fastdc.exceptions`. All inherit from `FastDCError`.

```python
from fastdc import FastDCError, ProviderNotConfigured, InvalidProvider
```

### FastDCError

Base exception for all FastDC errors.

### ProviderNotConfigured

Raised when `ai_chat()` is called with a provider that has not been registered via `add_ai_provider()`.

### InvalidProvider

Raised when `add_ai_provider()` is called with an unsupported provider name. Supported providers are `"groq"` and `"openai"`.

---

## Data Persistence

FastDC persists data to a JSON file (default: `fastdc_data.json`). The following data is persisted:

- Custom commands
- Auto-reply rules
- XP/leveling data
- Settings

Data is saved automatically every 5 minutes and can be triggered manually via `bot.save_state()` or the dashboard API.

The storage file path is configurable via the `data_file` parameter in the `FastBot` constructor:

```python
bot = FastBot(token="TOKEN", data_file="my_bot_data.json")
```
