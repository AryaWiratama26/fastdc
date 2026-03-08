<p align="center">
  <img src="/doc-ss/banner2.png" alt="FastDC Banner" />
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/fastdc" alt="PyPI - Version" />
  <img src="https://static.pepy.tech/badge/fastdc" alt="PyPI - Downloads" />
  <img src="https://github.com/AryaWiratama26/fastdc/actions/workflows/ci.yml/badge.svg" alt="CI Pipeline" />
  <img src="https://github.com/AryaWiratama26/fastdc/actions/workflows/publish.yml/badge.svg" alt="Publish to PyPI" />
</p>

**FastDC** is a Python library for building Discord bots quickly. All commands support both prefix (`!command`) and slash (`/command`) variants out of the box.

- Prefix and slash commands included by default
- AI integration (Groq and OpenAI)
- Moderation, utility, poll, ticket, giveaway, and reminder commands
- XP/leveling system, AFK status, starboard
- Auto-reply, anti-spam, auto-role, reaction roles, button roles
- Temp voice channels
- Embed builder and paginator utilities
- Web dashboard for managing bot settings
- JSON-based data persistence

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [Features](#features)
- [Dashboard](#dashboard)
- [Setup Requirements](#setup-requirements)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

```bash
pip install fastdc
```

Requirements: Python 3.10 or higher.

---

## Quick Start

```python
from fastdc import FastBot

bot = FastBot(token="YOUR_DISCORD_TOKEN")

# AI Chat
bot.add_ai_provider("groq", "YOUR_GROQ_API_KEY")
bot.ai_chat(provider="groq", context_file="data.txt")

# Commands
bot.setup_command_categories()
bot.add_moderation_commands()
bot.add_utility_commands()
bot.add_poll_commands()
bot.add_ticket_system()
bot.add_giveaway_commands()
bot.add_reminder_commands()
bot.add_custom_commands()
bot.enable_leveling()
bot.enable_afk_system()

# Events
bot.setup_event_logging()
bot.auto_reply(trigger="hi", response="Hello!")
bot.welcome_member()
bot.leave_member()
bot.enable_anti_spam(max_messages=5, interval=5, action="warn")

# Presence
bot.set_presence(activity_type="playing", activity_name="FastDC Bot")

bot.run()
```

---

## Commands

All commands are registered as both prefix (`!`) and slash (`/`) commands.

| Command | Description |
|---|---|
| `!ai` / `/ai` | Chat with the configured AI provider |
| `!kick` / `/kick` | Kick a member from the server |
| `!ban` / `/ban` | Ban a member from the server |
| `!clear` / `/clear` | Delete messages in bulk |
| `!ping` / `/ping` | Check bot latency |
| `!serverinfo` / `/serverinfo` | Display server information |
| `!bothelp` / `/help` | Show the help menu |
| `!poll` / `/poll` | Create a poll with emoji voting |
| `!ticket` / `/ticket` | Create a support ticket channel |
| `!close` / `/close` | Close a support ticket |
| `!giveaway` / `/giveaway` | Start a timed giveaway |
| `!remind` / `/remind` | Set a personal reminder |
| `!addcmd` / `/addcmd` | Create a custom command |
| `!delcmd` / `/delcmd` | Delete a custom command |
| `!listcmds` | List all custom commands |
| `!rank` / `/rank` | Check your XP rank |
| `!leaderboard` / `/leaderboard` | View the server XP leaderboard |
| `!afk` / `/afk` | Set your AFK status |
| `!rolepanel` / `/rolepanel` | Create a role picker panel |

---

## Features

See [docs.md](docs.md) for complete API reference with all method signatures and parameters.

### AI Integration

Supports Groq and OpenAI as AI providers. Optionally loads context from a text file for context-aware responses.

```python
bot.add_ai_provider("groq", "YOUR_API_KEY")
bot.ai_chat(provider="groq", context_file="knowledge.txt")
```

### Giveaway System

Timed giveaways with reaction entry. Duration supports `s`, `m`, `h`, `d` units (e.g. `1h`, `30m`). A random winner is selected when the timer expires.

```
!giveaway 1h "Discord Nitro"
```

### Leveling and XP

Users earn random XP per message. Level-up notifications are sent automatically. Includes `!rank` and `!leaderboard` commands.

```python
bot.enable_leveling(xp_per_message=15)
```

### Anti-Spam

Detects spam based on message frequency. Supports `mute`, `kick`, and `warn` actions.

```python
bot.enable_anti_spam(max_messages=5, interval=5, action="mute", mute_duration=300)
```

### Dashboard

A web-based control panel built with Quart. Manages bot settings, custom commands, auto-replies, and XP data through a browser interface and REST API.

```python
bot.enable_dashboard(port=5000, password="admin")
```

### Embed Utilities

```python
from fastdc import QuickEmbed, EmbedPaginator

# Create styled embeds
embed = QuickEmbed.success("Done", "Task completed.")
embed = QuickEmbed.error("Error", "Something went wrong.")
embed = QuickEmbed.warning("Warning", "Be careful.")
embed = QuickEmbed.info("Info", "For your information.")

# Paginated embeds
paginator = EmbedPaginator([embed1, embed2, embed3])
await ctx.send(embed=embed1, view=paginator)
```

---

## Dashboard

Enable the dashboard to manage the bot through a web browser:

```python
bot.enable_dashboard(port=5000, password="admin")
```

The dashboard runs concurrently with the bot using Hypercorn and provides:

- Settings management (prefix, anti-spam config)
- Custom command CRUD
- Auto-reply CRUD
- XP data management
- Manual save trigger

---

## Setup Requirements

1. Create a bot application at the [Discord Developer Portal](https://discord.com/developers/applications).
2. Enable **Privileged Gateway Intents** (Presence, Server Members, Message Content) in the Bot settings.
3. Generate a bot token and copy it.
4. For AI features, obtain an API key from [Groq](https://console.groq.com/) or [OpenAI](https://platform.openai.com/).

---

## Contributing

Contributions are welcome. Open an issue to discuss changes or submit a pull request.

## License

[MIT](LICENSE)