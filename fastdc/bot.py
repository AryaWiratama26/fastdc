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
        
        """
        
            Sets up an auto-reply feature for the bot. When a message containing the 
            specified trigger word or phrase is detected, the bot responds with the 
            provided response message.

            Parameters:
            ----------
            trigger : str
                The word or phrase that will trigger the auto-reply.
            
            response : str
                The message that the bot will send in response when the trigger is detected.
        """
        
        @self.bot.event
        async def on_message(message):
            if message.author.bot:
                return 
            if trigger.lower() in message.content.lower():
                await message.channel.send(response)
            await self.bot.process_commands(message)
            
    def ai_chat(self, api_key_usr):
        
        """
            This command allows users to interact with an LLM (LLaMA 3.3 70B) directly from Discord using the !ai command.

            Parameters:
            ----------
            api_key_usr : str
                Your Groq API key used to authenticate and access the AI model.
            
        """
        
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
        
        """
            Sets up a command to interact with a pre-trained conversational model 
            using the ChatterBot library.
        """
        @self.bot.command()
        async def askbot(ctx, *, message):
            response = self.trainer.get_response(message)
            await ctx.send(response)

    def run(self):
        """
            Starts the Discord bot using the provided token.
        """
        self.bot.run(self.token)
                    
