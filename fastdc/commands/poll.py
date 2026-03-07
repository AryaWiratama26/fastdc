"""
FastDC Poll Commands — Create interactive polls with emoji reactions
"""

import discord
from discord import app_commands
from discord.ext import commands

from ..utils.embed_builder import QuickEmbed

POLL_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']


def setup_poll_commands(bot_instance):
    """Register poll commands (prefix and slash)"""
    bot = bot_instance.bot

    # Prefix command: !poll "Question" "Option1" "Option2" ...
    @bot.command()
    async def poll(ctx, question: str, *options):
        if len(options) < 2:
            await ctx.send(embed=QuickEmbed.warning(
                "Not Enough Options",
                'Usage: `!poll "Question" "Option1" "Option2" ...`\nMinimum 2 options required.'
            ))
            return

        if len(options) > 10:
            await ctx.send(embed=QuickEmbed.warning(
                "Too Many Options",
                "Maximum 10 options allowed."
            ))
            return

        description = "\n\n".join(
            f"{POLL_EMOJIS[i]}  {option}" for i, option in enumerate(options)
        )

        embed = QuickEmbed.build(
            title=f"📊 {question}",
            description=description,
            color=QuickEmbed.PURPLE,
            footer=f"Poll by {ctx.author.display_name} • React to vote!",
            timestamp=True
        )

        poll_msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await poll_msg.add_reaction(POLL_EMOJIS[i])

    # Slash command: /poll
    @bot.tree.command(name='poll', description='Create a poll with up to 10 options')
    @app_commands.describe(
        question='The poll question',
        option1='Option 1 (required)',
        option2='Option 2 (required)',
        option3='Option 3',
        option4='Option 4',
        option5='Option 5',
    )
    async def poll_slash(
        interaction: discord.Interaction,
        question: str,
        option1: str,
        option2: str,
        option3: str = None,
        option4: str = None,
        option5: str = None,
    ):
        options = [opt for opt in [option1, option2, option3, option4, option5] if opt]

        description = "\n\n".join(
            f"{POLL_EMOJIS[i]}  {option}" for i, option in enumerate(options)
        )

        embed = QuickEmbed.build(
            title=f"📊 {question}",
            description=description,
            color=QuickEmbed.PURPLE,
            footer=f"Poll by {interaction.user.display_name} • React to vote!",
            timestamp=True
        )

        await interaction.response.send_message(embed=embed)
        poll_msg = await interaction.original_response()
        for i in range(len(options)):
            await poll_msg.add_reaction(POLL_EMOJIS[i])
