# ⚡ FastDC

<p align="center">
  <img src="https://img.shields.io/pypi/v/fastdc" alt="PyPI - Version" />
  <img src="https://img.shields.io/pypi/dm/fastdc" alt="PyPI - Downloads" />
</p>

**FastDC** is a powerful, modular, and AI-integrated Discord bot framework that helps you build feature-rich Discord bots effortlessly. With built-in support for multiple AI providers, command handling, moderation tools, and more, FastDC helps you go from idea to implementation in seconds.

---

## 📦 Installation

Install FastDC via pip:

```bash
pip install fastdc
```

---

## 🚀 Quick Start

```python
from fastdc import FastBot

bot = FastBot(token="YOUR_DISCORD_TOKEN")

# Setup AI providers
bot.add_ai_provider("groq", "YOUR_GROQ_API_KEY")
bot.add_ai_provider("openai", "YOUR_OPENAI_API_KEY")

# Enable AI chat with multiple providers
bot.ai_chat(provider="groq")  # or "openai"

# Setup command categories and help system
bot.setup_command_categories()

# Add moderation commands
bot.add_moderation_commands()

# Add utility commands
bot.add_utility_commands()

# Setup event logging
bot.setup_event_logging()

# Auto-reply feature
bot.auto_reply(trigger="hi", response="Hello!")

# Train the bot from a local file
bot.train_bot()  # Make sure 'data_train.txt' exists

# Trivia bot from json
bot.trivia_game(json_path="questions.json")

# Welcome and leave notifications
bot.welcome_member()
bot.leave_member()

# Run the bot
bot.run()
```

---

## 💬 Discord Commands

### 🤖 AI Commands
| Command            | Description                                              |
|--------------------|----------------------------------------------------------|
| `!ai {prompt}`     | Interact with AI using configured provider (Groq/OpenAI)  |
| `!askbot {question}` | Ask a question based on trained data                     |

### 🎮 Games
| Command            | Description                                              |
|--------------------|----------------------------------------------------------|
| `!trivia`          | Start trivia game                                        |
| `!trivia_score`    | Show trivia score                                        |
| `!trivia_leaderboard` | Show trivia leaderboard                              |

### 👮 Moderation
| Command            | Description                                              |
|--------------------|----------------------------------------------------------|
| `!kick @user [reason]` | Kick a user from the server                          |
| `!ban @user [reason]`  | Ban a user from the server                           |
| `!clear [amount]`      | Clear specified number of messages                    |

### ⚙️ Utility
| Command            | Description                                              |
|--------------------|----------------------------------------------------------|
| `!ping`            | Check bot latency                                        |
| `!serverinfo`      | Display server information                              |
| `!bothelp`         | Show help menu with all commands                        |

---

## 🔑 Discord Bot Token Setup

To create your bot, follow these steps:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application and add a bot.
3. Enable all **Privileged Gateway Intents**.

   ![Enable Intents](/doc-ss/intents.png)

---

## 🧠 AI Integration

FastDC supports multiple AI providers:

### Groq
- Visit [Groq Console](https://console.groq.com/)
- Sign in and generate your API key

### OpenAI
- Visit [OpenAI Platform](https://platform.openai.com/)
- Create an account and generate your API key

---

## 📁 Training Your Bot

The `train_bot()` method allows your bot to respond based on your own dataset.  
Simply create a file named `data_train.txt` in your project root with Q&A pairs.

**Example format**:
```
Q: What is FastDC?
A: FastDC is a Python library for creating Discord bots quickly.
```

---

## 👋 Member Join & Leave Events

Welcome and farewell messages are built-in.

```python
bot.welcome_member()
bot.leave_member()
```

These functions send automatic messages to the **system channel** when members join or leave the server:

- `welcome_member()` → `"Hello {username}, Welcome to Server!"`
- `leave_member()` → `"{username} has left the server 🖐️"`

---

## 🔍 Event Logging

FastDC includes a built-in logging system that tracks:
- Command usage
- Errors and exceptions
- Bot events
- AI interactions

Logs are formatted and can be easily integrated with your preferred logging system.

---

## 🙌 Contribution

Contributions are welcome!  
If you have ideas for improvements or new features, feel free to open an issue or submit a pull request.

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## ❤️ Support

If you like this project, consider giving it a ⭐ on GitHub or sharing it with others!

## 🌐 Website Documentation
[FastDC Website](https://fastdc.vercel.app/)

## Note : 
- This project will be updated regularly with new features and improvements
---