from fastdc import FastBot
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
BOT_KEY = os.getenv('API_BOT_KEY')

bot = FastBot(token=BOT_KEY)
bot.auto_reply(trigger="Hello Semuanya", response='Halo Juga')
bot.welcome_member()
bot.leave_member()
bot.trivia_game(json_path="questions.json")
bot.train_bot()
bot.ai_chat(api_key_usr=API_KEY)
bot.run()