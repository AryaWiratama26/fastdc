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

    # Setup AI providers
    bot.add_ai_provider("groq", GROQ_API_KEY)
    # bot.add_ai_provider("openai", OPENAI_API_KEY)
    
    bot.ai_chat(provider='groq')

    # Setup command categories and help system
    bot.setup_command_categories()

    # Add moderation commands
    bot.add_moderation_commands()

    # Add utility commands
    bot.add_utility_commands()

    # Setup event logging
    bot.setup_event_logging()

    # Add auto-reply feature
    bot.auto_reply(trigger="hi", response="Hello! How can I help you today?")

    # Train the bot from data_train.txt
    bot.train_bot()
    
    # Train ai with more data
    bot.custom_info_command(data_path="data.txt")

    # Setup welcome and leave messages
    bot.welcome_member()
    bot.leave_member()

    # Run the bot
    bot.run()

if __name__ == "__main__":
    main()