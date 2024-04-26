import discord
from discord.ext import commands
from discord import Button, User, ButtonStyle, SelectOption, SelectMenu
from discord.ui import Select, View
from typing import List, Union, Optional, Dict

from tools.tools import navigation_view


class Dropdown(discord.ui.Select):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

        # set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(
                label = option["label"],
                description = option["description"],
                emoji = option["emoji"],
                value = option["value"]
            )
            for option in self.bot.help_options
        ]

        super().__init__(placeholder='Sélectionnez une catégorie', min_values=1, max_values=1, options=options)
    
    def build_embed(self, title: str, description: str, page_commands: list, color: discord.Color = discord.Color.brand_green()):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)

        for command in page_commands:
            command = self.bot.get_command(command)
            if command is None:
                continue
            
            value = f"*{command.help if command.help else command.description}*"
            if command.aliases:
                value += f"\n`🔄️` Alias : {', '.join(command.aliases.copy())}"
            
            try:
                if command.extras["credits"]:
                    value += "\n`❤️` Crédits : "
                    for credit in command.extras["credits"]:
                        if isinstance(credit, int):
                            user = self.bot.get_user(credit)
                            value += user.name if user else f"`{credit}`"
                        else:
                            value += credit
            except KeyError:
                pass
            
            embed.add_field(
                name=f"`{self.bot.command_prefix}{command.usage}`",
                value=value,
                inline=False
            )
        return embed
    
    def build_pages(self, title: str, description: str, page_commands: list, color: discord.Color = discord.Color.brand_green()):
        embeds = []
        page_commands = page_commands.copy()

        divided_commands = [page_commands[i:i+5] for i in range(0, len(page_commands), 5) ]
        for commands in divided_commands:
            em = self.build_embed(title, description, commands, color)
            em.set_footer(text=f"Page {divided_commands.index(commands) + 1}/{len(divided_commands)}")
            embeds.append(em)
        return embeds
        

    async def callback(self, interaction: discord.Interaction):
        selected_option = interaction.data["values"][0]

        # Find the dict of the selected option
        selected_option = next(option for option in self.bot.help_options if option["value"] == selected_option)
        
        embeds = self.build_pages(
            title=f"Catégorie : {selected_option['label']}",
            description=selected_option['description'],
            page_commands=selected_option["commands"]
        )
        
        view = navigation_view(
            interaction.user,
            embeds,
            embeded=True,
            bot=self.bot,
            complex=False,
            custom_item=Dropdown(self.bot)
        )

        await interaction.response.edit_message(embed=embeds[0], view=view)

class DropdownView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__(timeout=360)
        
        self.add_item(Dropdown(self.bot))

class Help(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    def welcome_embed(self):
        embed = discord.Embed(
            title="Panel d'aide",
            description="Bienvenue !\n\nCe panel sert à t'aiguiller sur comment utiliser le bot.\n\nSynthaxe :\n`[argument]` = Argument obligatoire\n`<argument>` = Argument facultatif\nLes arguments `user` et `membre` doivent être une mention, si vous souhaitez mettre plusieurs mots à la suite il faut entourer l'argument par des guillemets : \"Mon argument\"",
            color=discord.Color.brand_green()
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        return embed


    @commands.command(name="help", aliases=["aide", "h"], help="Affiche l'aide", usage="help [commande]", description="Affiche l'aide de la commande spécifiée")
    async def help_command(self, ctx: commands.Context):
        embed = self.welcome_embed()

        self.bot.groups_def = {
            "staff": {
                "label": "Staff",
                "description": "Commandes utilisables par le staff du serveur",
                "emoji": "🎈",
                "value": "staff"
            },
            "a3": {
                "label": "A3",
                "description": "Commandes utilisables par les membres de grade A3",
                "emoji": "🔨",
                "value": "a3"
            },
            "fonda": {
                "label": "Fondateurs",
                "description": "Commandes utilisables par les fondateurs du serveur",
                "emoji": "👑",
                "value": "fonda"
            }
        }
        
        self.bot.help_options = [
            {
                "label": "Staff",
                "description": "Commandes réservées au staff du bot",
                "emoji": "🎈",
                "value": "staff",
                "commands": [
                    "me",
                    "connect",
                    "disconnect",
                ]
            },
            {
                "label": "A3",
                "description": "Commandes réservées aux membres de grade A3",
                "emoji": "🔨",
                "value": "a3",
                "commands": [
                    "check",
                    "leaderboard",
                ]
            },
            {
                "label": "Fondateurs",
                "description": "Commandes réservées aux fondateurs du serveur",
                "emoji": "👑",
                "value": "fonda",
                "commands": [
                    "add",
                    "remove",
                    "reset",
                    "delete",
                ]
            },
        ]

        for option in self.bot.help_options:
            embed.add_field(
                name=f"`{option['emoji']}` {option['label']}",
                value=option['description'],
                inline=False
            )
        
        await ctx.reply(embed=embed, view=DropdownView(self.bot))


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))