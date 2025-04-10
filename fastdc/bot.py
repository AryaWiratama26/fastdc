import discord
from discord.ext import commands
from .trainer import FastdcTrainer

class FastBot:
    def __init__(self, token: str, prefix: str = "!"):
        self.token = token
        self.bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
        self.trainer = FastdcTrainer()
        self.trainer.train()

    def auto_reply(self, trigger, response):
        @self.bot.event
        async def on_message(message):
            if message.author.bot:
                return 
            if trigger.lower() in message.content.lower():
                await message.channel.send(response)
            await self.bot.process_commands(message)
            
    def ai_chat(self, api_key_usr):
        from groq import Groq

        @self.bot.command()
        async def ai(ctx, *, prompt):
            
            client = Groq(api_key=api_key_usr)

            chat_completion = client.chat.completions.create(

                messages=[
                    {
                        "role": "system",
                        "content": "you are a helpful assistant."
                    },
                    
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],

                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_completion_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )

            await ctx.send(chat_completion.choices[0].message.content)
            
    def train_bot(self):
        @self.bot.command()
        async def askbot(ctx, *, message):
            response = self.trainer.get_response(message)
            await ctx.send(response)

    def run(self):
        self.bot.run(self.token)
                    
