"""
FastDC Button Roles — Discord component-based role picker
"""

import logging
import discord
from discord.ext import commands

from ..utils.embed_builder import QuickEmbed

logger = logging.getLogger('fastdc.button_roles')


class RoleButton(discord.ui.Button):
    """A button that toggles a role on click"""

    def __init__(self, role_id: int, label: str, emoji: str = None, style: discord.ButtonStyle = discord.ButtonStyle.primary):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=f"role_{role_id}")
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.role_id)
        if not role:
            await interaction.response.send_message("Role not found!", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                f"❌ Removed **{role.name}**",
                ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"✅ Added **{role.name}**",
                ephemeral=True
            )


class RoleSelectMenu(discord.ui.Select):
    """A dropdown menu for selecting roles"""

    def __init__(self, roles: list, placeholder: str = "Select a role..."):
        options = [
            discord.SelectOption(label=label, value=str(role_id), emoji=emoji)
            for role_id, label, emoji in roles
        ]
        super().__init__(placeholder=placeholder, options=options, custom_id="role_select")

    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)
        if not role:
            await interaction.response.send_message("Role not found!", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                f"❌ Removed **{role.name}**",
                ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"✅ Added **{role.name}**",
                ephemeral=True
            )


class RoleView(discord.ui.View):
    """Persistent view for role buttons/dropdowns"""

    def __init__(self):
        super().__init__(timeout=None)


def setup_button_roles(bot_instance):
    """Register button/dropdown role commands"""
    bot = bot_instance.bot

    @bot.command(name='rolepanel')
    @commands.has_permissions(manage_roles=True)
    async def rolepanel(ctx, panel_type: str = "buttons"):
        """Create a role panel. Usage: !rolepanel buttons OR !rolepanel dropdown"""
        if not bot_instance._button_role_configs:
            await ctx.send(embed=QuickEmbed.warning(
                "No Roles Configured",
                "Use `bot.add_button_role()` to configure roles first."
            ))
            return

        view = RoleView()

        if panel_type == "dropdown":
            roles_list = [
                (cfg['role_id'], cfg['label'], cfg.get('emoji'))
                for cfg in bot_instance._button_role_configs
            ]
            view.add_item(RoleSelectMenu(roles_list, placeholder="Pick a role..."))
        else:
            for cfg in bot_instance._button_role_configs:
                style = getattr(discord.ButtonStyle, cfg.get('style', 'primary'), discord.ButtonStyle.primary)
                view.add_item(RoleButton(
                    role_id=cfg['role_id'],
                    label=cfg['label'],
                    emoji=cfg.get('emoji'),
                    style=style
                ))

        embed = QuickEmbed.build(
            title="🎭 Role Picker",
            description="Click a button or select from the dropdown to toggle roles!",
            color=QuickEmbed.PURPLE
        )
        await ctx.send(embed=embed, view=view)

    @bot.tree.command(name='rolepanel', description='Create a role picker panel')
    @discord.app_commands.describe(panel_type='Panel type: buttons or dropdown')
    @discord.app_commands.checks.has_permissions(manage_roles=True)
    async def rolepanel_slash(interaction: discord.Interaction, panel_type: str = "buttons"):
        if not bot_instance._button_role_configs:
            await interaction.response.send_message(embed=QuickEmbed.warning(
                "No Roles Configured",
                "Use `bot.add_button_role()` to configure roles first."
            ), ephemeral=True)
            return

        view = RoleView()

        if panel_type == "dropdown":
            roles_list = [
                (cfg['role_id'], cfg['label'], cfg.get('emoji'))
                for cfg in bot_instance._button_role_configs
            ]
            view.add_item(RoleSelectMenu(roles_list, placeholder="Pick a role..."))
        else:
            for cfg in bot_instance._button_role_configs:
                style = getattr(discord.ButtonStyle, cfg.get('style', 'primary'), discord.ButtonStyle.primary)
                view.add_item(RoleButton(
                    role_id=cfg['role_id'],
                    label=cfg['label'],
                    emoji=cfg.get('emoji'),
                    style=style
                ))

        embed = QuickEmbed.build(
            title="🎭 Role Picker",
            description="Click a button or select from the dropdown to toggle roles!",
            color=QuickEmbed.PURPLE
        )
        await interaction.response.send_message(embed=embed, view=view)
