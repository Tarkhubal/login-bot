import discord
from discord.ext import commands
from discord import app_commands
from typing import Union, Optional

from tools import tools as tl
from tools.configs import Configs
from tools.database import Database
from tools.checks import is_staff, is_a3, is_owner



class view1(discord.ui.View):
    def __init__(self, bot: commands.Bot, author: Union[discord.User, discord.Member], embed: discord.Embed):
        if isinstance(author, discord.Member):
            author = author._user
        self.bot = bot
        self.author = author
        self.embed = embed
        super().__init__()

    async def interaction_check(self, interaction: discord.Interaction):
        return (interaction.user == self.author)

    @discord.ui.button(label="Afficher quand même", row=0)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = view2(self.bot, interaction.user)
        self.embed.color = discord.Color.red()
        await interaction.response.edit_message(content=None, embed=self.embed, view=view)
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
        await interaction.message.delete()
        self.stop()
    




class Connexions(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.db: Database = bot.database
    
    @is_staff()
    @commands.hybrid_command(name="me", description="Voir son nombre de connexions", with_app_command=True)
    async def me(self, ctx: commands.Context):
        try:
            q = self.db.get.nb_connexions(ctx.author.id)
        except:
            q = 0
        
        desc = f"Vous avez actuellement {q} connexion{tl.pl(q)}."
        embed = discord.Embed(
            title="Vos connexions",
            description=desc,
            color=discord.Color.blurple()
        )
        try:
            await ctx.author.send(embed=embed)
        except:
            return await ctx.reply(content=f"{ctx.author.mention}, je ne peux pas vous envoyer de message privé.", view=view1(self.bot, ctx.author, embed))
        await ctx.reply(content=f"{ctx.author.mention}, regarde en MP !")
    
    @is_a3()
    @commands.hybrid_command(name="check", description="Voir le nombre de connexions d'un membre", with_app_command=True)
    async def check(self, ctx: commands.Context, member: Union[discord.Member, discord.User]):
        try:
            q = self.db.get.nb_connexions(member.id)
        except:
            q = 0
        
        desc = f"{member.mention} a actuellement {q} connexion{tl.pl(q)}."
        embed = discord.Embed(
            title="Connexions",
            description=desc,
            color=discord.Color.blurple()
        )
        await ctx.reply(embed=embed)
    


async def setup(bot: commands.Bot):
    await bot.add_cog(Connexions(bot))
