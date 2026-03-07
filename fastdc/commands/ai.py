"""
FastDC AI Commands — Prefix + Slash commands for AI chat
"""

import logging
import discord
from discord import app_commands
from discord.ext import commands

from ..utils.helpers import load_knowledge, find_relevant_info

logger = logging.getLogger('fastdc.ai')


def setup_ai_commands(bot_instance, provider: str, context_file: str = None):
    """
    Register AI chat commands (prefix !ai and slash /ai).

    Parameters:
    ----------
    bot_instance : FastBot
        The FastBot instance
    provider : str
        AI provider to use ('groq' or 'openai')
    context_file : str, optional
        Path to knowledge file for context-aware responses
    """
    bot = bot_instance.bot
    ai_provider = bot_instance.ai_providers[provider]
    client = ai_provider.client

    def _build_prompt(user_prompt: str) -> str:
        if not context_file:
            return user_prompt

        entries = load_knowledge(context_file)
        context = find_relevant_info(user_prompt, entries)

        if context:
            return (
                f"Use the following information to answer the user's question:\n"
                f"{context}\n\n"
                f"Question: {user_prompt}\n"
                f"Answer clearly and specifically."
            )
        return user_prompt

    async def _get_ai_response(prompt: str) -> str:
        """Get response from the configured AI provider"""
        final_prompt = _build_prompt(prompt)

        if provider == 'groq':
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": final_prompt}
                ],
                model=ai_provider.model or "llama-3.3-70b-versatile",
                temperature=0.5,
                max_completion_tokens=1024
            )
        elif provider == 'openai':
            response = client.chat.completions.create(
                model=ai_provider.model or "gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": final_prompt}
                ]
            )

        return response.choices[0].message.content

    @bot.command(name='ai')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ai_prefix(ctx, *, prompt):
        async with ctx.typing():
            try:
                result = await bot.loop.run_in_executor(None, lambda: _get_ai_response.__wrapped__(prompt) if hasattr(_get_ai_response, '__wrapped__') else None)
                if result is None:
                    result = _build_prompt(prompt)
                    if provider == 'groq':
                        response = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": result}
                            ],
                            model=ai_provider.model or "llama-3.3-70b-versatile",
                            temperature=0.5,
                            max_completion_tokens=1024
                        )
                    elif provider == 'openai':
                        response = client.chat.completions.create(
                            model=ai_provider.model or "gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": result}
                            ]
                        )
                    result = response.choices[0].message.content

                if len(result) > 2000:
                    for i in range(0, len(result), 2000):
                        await ctx.send(result[i:i+2000])
                else:
                    await ctx.send(result)
            except Exception as e:
                logger.error(f"AI chat error: {str(e)}")
                await ctx.send("An error occurred while processing your request.")

    @bot.tree.command(name='ai', description='Chat with AI assistant')
    @app_commands.describe(prompt='Your message or question for the AI')
    async def ai_slash(interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        try:
            final = _build_prompt(prompt)

            if provider == 'groq':
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": final}
                    ],
                    model=ai_provider.model or "llama-3.3-70b-versatile",
                    temperature=0.5,
                    max_completion_tokens=1024
                )
            elif provider == 'openai':
                response = client.chat.completions.create(
                    model=ai_provider.model or "gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": final}
                    ]
                )

            result = response.choices[0].message.content
            if len(result) > 2000:
                await interaction.followup.send(result[:2000])
            else:
                await interaction.followup.send(result)
        except Exception as e:
            logger.error(f"AI slash error: {str(e)}")
            await interaction.followup.send("An error occurred while processing your request.")
