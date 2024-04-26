import discord
from discord.ext import commands
from typing import Union


def generate_embed(data: dict):
    _data = data['content']
    if 'medias' in data:
        if 'thumbnail' in data['medias']:
            _data['thumbnail'] = {'url': data['medias']['thumbnail']}
        if 'video' in data['medias']:
            _data['video'] = {'url': data['medias']['video']}
        if 'image' in data['medias']:
            _data['image'] = {'url': data['medias']['image']}
    if 'fields' in data:
        _data['fields'] = data['fields']
    if 'footer' in data:
        _data['footer'] = {}
        _data['footer']['icon_url'] = data['footer']['img']
        _data['footer']['text'] = data['footer']['text']
    if 'author' in data:
        _data['author'] = {}
        _data['author']['name'] = data['author']['text']
    if 'color' in _data:
        _data['color'] = int(_data['color'].replace('#', ''), 16)

    return discord.Embed().from_dict(_data)


class view1(discord.ui.View):
    def __init__(self, bot: commands.Bot, author: Union[discord.User, discord.Member]):
        if isinstance(author, discord.Member):
            author = author._user
        self.bot = bot
        self.author = author
        super().__init__()

    async def interaction_check(self, interaction: discord.Interaction):
        return (interaction.user == self.author)

    @discord.ui.button(label="Afficher quand même", row=0)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = generate_embed({'type': 'embed', 'content': {'title': 'help', 'description': 'yes', 'color': '#ff0000', 'type': 'rich'}})
        view = view2(self.bot, interaction.user)
        content = None
        await interaction.response.edit_message(content=content, embed=embed, view=view)
        self.stop()
    

class view2(discord.ui.View):
    def __init__(self, bot: commands.Bot, author: Union[discord.User, discord.Member]):
        if isinstance(author, discord.Member):
            author = author._user
        self.bot = bot
        self.author = author
        super().__init__()

    async def interaction_check(self, interaction: discord.Interaction):
        return (interaction.user == self.author)

    @discord.ui.button(label="Supprimer le message", row=0)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = generate_embed({'type': 'embed', 'content': {'title': 'help', 'description': 'yes', 'color': '#ff0000', 'type': 'rich'}})
        view = None
        content = None
        await interaction.response.edit_message(content=content, embed=embed, view=view)
        self.stop()
    
