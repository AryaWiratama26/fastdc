<p align="center">
  <img src="https://img.shields.io/pypi/v/fastdc" alt="PyPI - Version" />
  <img src="https://img.shields.io/pypi/dm/fastdc" alt="PyPI - Downloads" />
  <img src="https://github.com/AryaWiratama26/fastdc/actions/workflows/ci.yml/badge.svg" alt="CI Pipeline" />
  <img src="https://github.com/AryaWiratama26/fastdc/actions/workflows/publish.yml/badge.svg" alt="Publish to PyPI" />
</p>

**FastDC** — A powerful library for creating Discord bots quickly. All commands have **prefix** + **slash** support.

---

## Installation

```bash
pip install fastdc
```

## Quick Start

```python
from fastdc import FastBot

bot = FastBot(token="YOUR_TOKEN")
bot.add_ai_provider("groq", "API_KEY")
bot.ai_chat(provider="groq")
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
bot.setup_event_logging()
bot.auto_reply(trigger="hi", response="Hello!")
bot.welcome_member()
bot.leave_member()
bot.enable_anti_spam(max_messages=5, interval=5, action="warn")
bot.set_presence(activity_type="playing", activity_name="FastDC")
bot.run()
```

## Commands

| Command | Description |
|---|---|
| `!ai` `/ai` | AI chat |
| `!kick` `!ban` `!clear` | Moderation |
| `!ping` `!serverinfo` `!bothelp` | Utility |
| `!poll` `/poll` | Polls |
| `!ticket` `!close` | Tickets |
| `!giveaway` `/giveaway` | Giveaways |
| `!remind` `/remind` | Reminders |
| `!addcmd` `!delcmd` `!listcmds` | Custom commands |
| `!rank` `!leaderboard` | Leveling |
| `!afk` `/afk` | AFK status |
| `!rolepanel` `/rolepanel` | Button roles |

## Features

- **AI** — Groq + OpenAI with optional knowledge context
- **Giveaway** — Timed with random winner
- **Reminder** — DM after delay
- **Custom Commands** — Admin creates/deletes at runtime
- **Leveling** — XP per message, rank card, leaderboard
- **AFK** — Status + auto-notify on mention
- **Starboard** — Popular messages reposted
- **Temp Voice** — Auto-create/delete VCs
- **Button Roles** — Discord component role picker
- **Anti-Spam** — Mute/kick/warn on spam
- **Embed Builder** — QuickEmbed helpers
- **Paginator** — Multi-page embeds with buttons
- **Scheduler** — Delayed messages

## Setup

1. [Discord Developer Portal](https://discord.com/developers/applications)
2. **Groq**: [console.groq.com](https://console.groq.com/) | **OpenAI**: [platform.openai.com](https://platform.openai.com/)

## License
[MIT](LICENSE)