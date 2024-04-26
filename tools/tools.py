import datetime
import json
import discord

from discord import ButtonStyle, User
from discord.ext import commands
from discord.ui import View, Button, button
from typing import Union, List

def get_date():
    return datetime.datetime.now()

def datetime_to_unix(date: datetime.datetime) -> int:
    return int(date.timestamp())

def unix_to_datetime(date: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(date)

def thisdate_to_unix():
    return datetime_to_unix(get_date())

def get_config() -> dict:
    with open("configs.json", "r") as file:
        return json.load(file)

def listplural(data: Union[list, int], word: str = "") -> str:
    if isinstance(data, int):
        return f"{word}{'s' if data > 1 else ''}"
    return f"{word}{'s' if len(data) > 1 else ''}"

def pl(data: Union[list, int], word: str = "") -> str:
    return listplural(data, word)

def chunk_list(data: list, size: int) -> list:
    """Separate a list into chunks of a certain size"""
    return [data[i:i + size] for i in range(0, len(data), size)]



class navigation_view(View):
    def __init__(self, author: User, pages: List[Union[discord.Embed, str]], embeded: bool, bot: commands.Bot = None, complex: int = False, custom_item: discord.ui.Item = None):
        """Une view pour naviguer entre les pages d'un embed ou d'un message

        Args:
            - author (User): l'auteur du message (doit être UNIQUEMENT un User)
            - pages (List[Union[discord.Embed, str]]): la liste des pages (embeds, strings, etc.)
            - embeded (bool): `True` si les pages sont des embeds, `False` si ce sont des strings (ou autre)
        """
        super().__init__(timeout=None)
        self.bot = bot if bot else None
        self.author = author
        self.pages = pages
        self.embeded = embeded
        self.complex = complex

        self.current_page = 0
        self.clear_items()
        
        if len(self.pages) == 1:
            self.add_item(self.quit)
        else:
            self.add_item(self.past)
            self.add_item(self.previous)
            self.add_item(self.next)
            self.add_item(self.future)
            self.add_item(self.quit)
            
            if complex or len(self.pages) > 2:
                self.add_item(self.first)
                self.add_item(self.last)
            
            if (not complex and len(self.pages) == 2) or (complex and len(self.pages) < 5):
                self.remove_item(self.past)
                self.remove_item(self.future)

        if custom_item:
            self.add_item(custom_item)

        self.add_item(discord.ui.Button(label=f"Page {self.current_page + 1}/{len(self.pages)}", style=ButtonStyle.green, disabled=True, row=1 if (len(self.pages) == 1) or (not complex and len(self.pages) == 2) else 2))


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return (interaction.user.id == self.author.id)
    
    async def on_timeout(self) -> None:
        try:
            await self.message.delete()
        except:
            pass


    async def update_children(self, interaction: discord.Interaction):
        self.previous.disabled = (self.current_page <= 0)
        self.first.disabled = (self.current_page <= 0)
        self.past.disabled = (self.current_page <= 0)
        self.next.disabled = (self.current_page + 1 == len(self.pages))
        self.last.disabled = (self.current_page + 1 == len(self.pages))
        self.future.disabled = (self.current_page + 1 == len(self.pages))

        try:
            kwargs = {'content': str(self.pages[self.current_page])} if not (self.embeded) else {'embed': self.pages[self.current_page]}
        except:
            kwargs = {'content': str(self.pages[0])} if not (self.embeded) else {'embed': self.pages[0]}
        
        self.children[-1].label = f"Page {self.current_page + 1}/{len(self.pages)}"
        kwargs['view'] = self

        await interaction.response.edit_message(**kwargs)
    
    @button(label="◀◀", style=ButtonStyle.gray, row=1)
    async def past(self, interaction: discord.Interaction, button: Button):
        if self.complex and self.current_page >= 5:
            self.current_page -= 5
        else:
            self.current_page = 0
        
        await self.update_children(interaction)

    @button(label="◀", style=ButtonStyle.blurple, row=1)
    async def previous(self, interaction: discord.Interaction, button: Button):
        self.current_page -= 1

        await self.update_children(interaction)

    @button(label="▶", style=ButtonStyle.blurple, row=1)
    async def next(self, interaction: discord.Interaction, button: Button):
        self.current_page += 1

        await self.update_children(interaction)

    @button(label="▶▶", style=ButtonStyle.gray, row=1)
    async def future(self, interaction: discord.Interaction, button: Button):
        if self.complex is False:
            self.current_page = len(self.pages) - 1
        else:
            if self.current_page <= (len(self.pages) - 5):
                self.current_page += 5
            else:
                self.current_page = len(self.pages)

        await self.update_children(interaction)


    @button(label="Quitter", style=ButtonStyle.red, row=1)
    async def quit(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="Navigation terminée.", view=None)
        self.stop()
    
    @button(label="First page", style=ButtonStyle.green, row=2)
    async def first(self, interaction: discord.Interaction, button: Button):
        self.current_page = 0

        await self.update_children(interaction)
    
    @button(label="Last page", style=ButtonStyle.green, row=2)
    async def last(self, interaction: discord.Interaction, button: Button):
        self.current_page = len(self.pages) - 1

        await self.update_children(interaction)