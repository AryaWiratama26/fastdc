# ⚡ FastDC

<p align="center">
  <img src="/doc-ss/banner.png" alt="FastDC Banner" width="100%">
</p>

**FastDC** is a lightweight and powerful Python library designed to help you build Discord bots effortlessly. With built-in support for command handling, AI chat, bot training, and more, FastDC helps you go from idea to implementation in seconds.

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

# Auto-reply feature
bot.auto_reply(trigger="hi", response="Hello!")

# Enable AI chat with Groq API
bot.ai_chat(api_key_usr="YOUR_GROQ_API_KEY")

# Train the bot from a local file
bot.train_bot()  # Make sure 'data_train.txt' exists

# Welcome and leave notifications
bot.welcome_member()
bot.leave_member()

# Run the bot
bot.run()
```

---

## 💬 Discord Commands

| Command            | Description                                              |
|--------------------|----------------------------------------------------------|
| `!askbot {question}` | Ask a question based on trained data (`data_train.txt`) |
| `!ai {prompt}`     | Interact with an AI using Groq API                        |

---

## 🔑 Discord Bot Token Setup

To create your bot, follow these steps:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application and add a bot.
3. Enable all **Privileged Gateway Intents**.

   ![Enable Intents](/doc-ss/intents.png)

---

## 🧠 Groq AI API Key

To use the `!ai` command, you'll need an API key from Groq:

- Visit [Groq Console](https://console.groq.com/)
- Sign in and generate your API key

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

## 👀 Preview

<p align="center">
  <img src="/doc-ss/preview.png" alt="FastDC Bot on discord" width="80%">
</p>

## 🙌 Contribution

Contributions are welcome!  
If you have ideas for improvements or new features, feel free to open an issue or submit a pull request.

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## ❤️ Support

If you like this project, consider giving it a ⭐ on GitHub or sharing it with others!

---