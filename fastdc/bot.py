import discord
from discord.ext import commands
from .trainer import FastdcTrainer
import random
import json

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
            
    def welcome_member(self):
        
        """
            Sends a welcome message to new members who join the Discord server.
            The message is sent in the server's system channel if it exists.
        """
        
        @self.bot.event
        async def on_member_join(member):
            channel = member.guild.system_channel
            
            if not channel:
                for ch in member.guild.text_channels:
                    if ch.permissions_for(member.guild.me).send_messages:
                        channel = ch
                        break
                    
            if channel:
                await channel.send(f"Hello {member.name}, Welcome to Server! 👋")
                
    def leave_member(self):
        
        """
            Sends a farewell message to the system channel (or first accessible channel) 
            when a member leaves the server.
        """
        
        @self.bot.event
        async def on_member_remove(member):
            channel = member.guild.system_channel
            
            if not channel:
                for ch in member.guild.text_channels:
                    if ch.permissions_for(member.guild.me).send_messages:
                        channel = ch
                        break
            
            if channel:
                await channel.send(f"{member.name} has left the server 🖐️")
            
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
            
    def trivia_game(self, json_path="trivia_questions.json"):
        
        """
        Adds a trivia game command with categories, score tracking, and leaderboard.
        Questions are loaded from a JSON file.
        """
        self.scores = {}
        with open(json_path, "r") as file:
            all_questions = json.load(file)

        @self.bot.command()
        async def trivia(ctx, category=None):
            questions = all_questions
            if category:
                questions = [q for q in all_questions if q["category"].lower() == category.lower()]
                if not questions:
                    await ctx.send("❌ No questions found in that category.")
                    return

            q = random.choice(questions)
            embed = discord.Embed(title="🧠 Trivia Time!", description=q["question"], color=0x38bdf8)
            embed.add_field(name="Options", value="\n".join(q["options"]), inline=False)
            embed.set_footer(text="Reply with A, B, C, or D")

            await ctx.send(embed=embed)

            def check(m):
                return (
                    m.author == ctx.author
                    and m.channel == ctx.channel
                    and m.content.upper() in ["A", "B", "C", "D"]
                )

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=20.0)
                if msg.content.upper() == q["answer"]:
                    await ctx.send("✅ Correct!")
                    self.scores[msg.author.name] = self.scores.get(msg.author.name, 0) + 1
                else:
                    await ctx.send(f"❌ Wrong! The correct answer was {q['answer']}")
            except:
                await ctx.send("⌛ Time's up!")

        @self.bot.command()
        async def trivia_score(ctx):
            score = self.scores.get(ctx.author.name, 0)
            await ctx.send(f"🎯 {ctx.author.name}, your score is **{score}**.")

        @self.bot.command()
        async def trivia_leaderboard(ctx):
            if not self.scores:
                await ctx.send("📉 No scores yet.")
                return
            sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
            leaderboard = "\n".join([f"🏅 {user}: {score}" for user, score in sorted_scores[:5]])
            await ctx.send(f"📊 **Leaderboard**\n{leaderboard}")

    def run(self):
        """
            Starts the Discord bot using the provided token.
        """
        self.bot.run(self.token)
                    
