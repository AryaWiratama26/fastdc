from fastdc import FastBot
import os
from dotenv import load_dotenv

load_dotenv()

# Get tokens from environment variables
DISCORD_TOKEN = os.getenv('API_BOT_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def main():
    # Initialize the bot
    bot = FastBot(token=DISCORD_TOKEN)

    # Setup AI provider
    bot.add_ai_provider("groq", GROQ_API_KEY)
    # bot.add_ai_provider("openai", OPENAI_API_KEY)

    # Enable AI chat with optional context file
    bot.ai_chat(provider='groq', context_file='data.txt')

    # Setup command categories and help system
    bot.setup_command_categories()

    # Add moderation commands (prefix + slash)
    bot.add_moderation_commands()

    # Add utility commands (prefix + slash)
    bot.add_utility_commands()

    # Add poll system (prefix + slash)
    bot.add_poll_commands()

    # Add ticket system (prefix + slash)
    bot.add_ticket_system()

    # Add giveaway system
    bot.add_giveaway_commands()

    # Add reminder system
    bot.add_reminder_commands()

    # Add custom commands (!addcmd, !delcmd, !listcmds)
    bot.add_custom_commands()

    # Enable leveling/XP system
    bot.enable_leveling(xp_per_message=15)

    # Enable AFK system
    bot.enable_afk_system()

    # Setup event logging
    bot.setup_event_logging()

    # Auto-reply (supports multiple triggers)
    bot.auto_reply(trigger="hi", response="Hello! How can I help you today?")
    bot.auto_reply(trigger="bye", response="Goodbye! See you later!")

    # Setup welcome and leave messages
    bot.welcome_member()
    bot.leave_member()

    # Auto role (uncomment and set your role ID)
    # bot.auto_role(role_id=123456789)

    # Reaction roles (uncomment and set your own IDs)
    # bot.add_reaction_role(message_id=123456, emoji="👍", role_id=789012)
    # bot.enable_reaction_roles()

    # Button roles (uncomment and set your role IDs)
    # bot.add_button_role(role_id=111, label="Gamer", emoji="🎮")
    # bot.add_button_role(role_id=222, label="Artist", emoji="🎨")
    # bot.enable_button_roles()

    # Starboard (uncomment and set your channel ID)
    # bot.enable_starboard(channel_id=123456, emoji="⭐", threshold=3)

    # Temp voice channels (uncomment and set your channel ID)
    # bot.enable_temp_voice(trigger_channel_id=123456)

    # Anti-spam (optional)
    bot.enable_anti_spam(max_messages=5, interval=5, action="warn")

    # Set bot presence/status
    bot.set_presence(
        status="online",
        activity_type="playing",
        activity_name="FastDC v2.2"
    )
    # Enable web dashboard at http://localhost:5000
    bot.enable_dashboard(port=5000, password="admin123")

    # Run the bot
    bot.run(message_run="si {bot} ready")


if __name__ == "__main__":
    main()