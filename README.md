<p align="center">
  <img src="/doc-ss/banner2.png" alt="Banner-Logo" />
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/fastdc" alt="PyPI - Version" />
  <img src="https://static.pepy.tech/badge/fastdc" alt="PyPI - Downloads" />
  <img src="https://github.com/AryaWiratama26/fastdc/actions/workflows/ci.yml/badge.svg" alt="CI Pipeline" />
  <img src="https://github.com/AryaWiratama26/fastdc/actions/workflows/publish.yml/badge.svg" alt="Publish to PyPI" />
</p>

**FastDC** is a powerful library for creating Discord bots quickly. All commands support both **prefix** and **slash** variants.

---

## Installation

```bash
pip install fastdc
```

---

## Quick Start

```python
from fastdc import FastBot

bot = FastBot(token="YOUR_DISCORD_TOKEN")

# AI (Groq or OpenAI)
bot.add_ai_provider("groq", "YOUR_GROQ_API_KEY")
bot.ai_chat(provider="groq", context_file="data.txt")

# Commands
bot.setup_command_categories()
bot.add_moderation_commands()      # kick, ban, clear
bot.add_utility_commands()         # ping, serverinfo
bot.add_poll_commands()            # poll with emoji voting
bot.add_ticket_system()            # support tickets
bot.add_giveaway_commands()        # timed giveaways
bot.add_reminder_commands()        # DM reminders
bot.add_custom_commands()          # admin-created commands
bot.enable_leveling()              # XP system + leaderboard
bot.enable_afk_system()            # AFK status

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

## All Commands

| Command | Description |
|---|---|
| `!ai` / `/ai` | Chat with AI |
| `!kick` / `/kick` | Kick member |
| `!ban` / `/ban` | Ban member |
| `!clear` / `/clear` | Clear messages |
| `!ping` / `/ping` | Check latency |
| `!serverinfo` / `/serverinfo` | Server info |
| `!bothelp` / `/help` | Help menu |
| `!poll` / `/poll` | Create polls |
| `!ticket` / `/ticket` | Create support ticket |
| `!close` / `/close` | Close ticket |
| `!giveaway` / `/giveaway` | Start a giveaway |
| `!remind` / `/remind` | Set a reminder |
| `!addcmd` / `/addcmd` | Create custom command |
| `!delcmd` / `/delcmd` | Delete custom command |
| `!listcmds` | List custom commands |
| `!rank` / `/rank` | Check XP rank |
| `!leaderboard` / `/leaderboard` | XP leaderboard |
| `!afk` / `/afk` | Set AFK status |
| `!rolepanel` / `/rolepanel` | Create role picker |

---

## Features

### AI Integration
```python
bot.add_ai_provider("groq", "API_KEY")
bot.ai_chat(provider="groq", context_file="data.txt")
```

### Giveaway System
```
!giveaway 1h "Discord Nitro"
```
Timed giveaway with reaction entry and random winner selection.

### Reminders
```
!remind 30m Check the oven
```
Bot DMs you after the specified time.

### Custom Commands
```
!addcmd hello Hello everyone!    → creates !hello
!delcmd hello                    → removes !hello
!listcmds                        → list all custom commands
```

### Leveling/XP System
```python
bot.enable_leveling(xp_per_message=15)
```
Users gain XP per message, level up notifications, `!rank` and `!leaderboard`.

### AFK System
```python
bot.enable_afk_system()
```
`!afk reason` → Bot notifies when someone mentions an AFK user.

### Starboard
```python
bot.enable_starboard(channel_id=123, emoji="⭐", threshold=3)
```
Messages with enough star reactions get reposted to a starboard channel.

### Temp Voice Channels
```python
bot.enable_temp_voice(trigger_channel_id=123)
```
Join a trigger channel → get your own VC → auto-deletes when empty.

### Button/Dropdown Roles
```python
bot.add_button_role(role_id=111, label="Gamer", emoji="🎮")
bot.add_button_role(role_id=222, label="Artist", emoji="🎨")
bot.enable_button_roles()
# Then use !rolepanel or /rolepanel
```

### Auto Role
```python
bot.auto_role(role_id=123)
```

### Anti-Spam
```python
bot.enable_anti_spam(max_messages=5, interval=5, action="mute")
```

### Embed Paginator
```python
from fastdc import EmbedPaginator
paginator = EmbedPaginator([embed1, embed2, embed3])
await ctx.send(embed=embed1, view=paginator)
```

### Embed Builder
```python
from fastdc import QuickEmbed
embed = QuickEmbed.success("Done!", "Task completed.")
embed = QuickEmbed.error("Error", "Something went wrong.")
```

### Scheduled Messages
```python
bot.schedule_message(channel_id=123, message="Reminder!", delay_seconds=3600)
```

---

## Setup

1. [Discord Developer Portal](https://discord.com/developers/applications) → Create bot → Enable Privileged Intents
2. **Groq**: [console.groq.com](https://console.groq.com/) | **OpenAI**: [platform.openai.com](https://platform.openai.com/)

---

## Contribution

Contributions welcome! Open an issue or submit a PR.

## License

[MIT](LICENSE)

## Support

Give it a star on GitHub if you like this project!