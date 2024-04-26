import discord
from discord.ext import commands
from discord import app_commands
from typing import Union, Optional

from tools import tools as tl
from tools.database import Database
from tools.checks import is_staff, is_a3


async def disconnect_check(bot: commands.Bot, ctx: Union[commands.Context, discord.Interaction]):
    if ctx.author.id not in ctx.bot.connexions or bot.connexions[ctx.author.id] is False:
        em = discord.Embed(
            title="Aucune connexion en cours",
            description=f"Vous n'avez pas de connexion en cours.\n\nUtilisez `/connect`, `{ctx.bot.command_prefix}connect` ou le bouton ci-dessous pour en démarrer une.",
            color=discord.Color.red()
        )
    else:
        em = discord.Embed(
            title="Connexion terminée",
            description=f"Votre connexion a été terminée avec succès.\n\nUtilisez `/connect`, `{ctx.bot.command_prefix}connect` ou le bouton ci-dessous pour en démarrer une nouvelle.",
            color=discord.Color.green()
        )
    
    bot.connexion[ctx.author.id] = False
    view = StartConn(ctx.bot, ctx.author)
    if isinstance(ctx, commands.Context):
        return await ctx.reply(embed=em, view=view)
    return await ctx.response.edit_message(embed=em, view=view)

async def connect_check(bot: commands.Bot, ctx: Union[commands.Context, discord.Interaction]):
    if ctx.author.id in bot.connexions and bot.connexions[ctx.author.id] is True:
        em = discord.Embed(
            title="Connexion en cours",
            description=f"Vous avez déjà une connexion en cours.\n\nUtilisez `/disconnect`, `{bot.command_prefix}disconnect` ou le bouton ci-dessous pour la terminer.",
            color=discord.Color.red()
        )
        view = CloseConn(bot, ctx.author)
        if isinstance(ctx, commands.Context):
            return await ctx.reply(embed=em, view=view)
        return await ctx.response.edit_message(embed=em, view=view)
    
    bot.connexions[ctx.author.id] = True
    em = discord.Embed(
        title="Connexion démarrée",
        description=f"Vous avez démarré une connexion.\n\nUtilisez `/disconnect`, `{bot.command_prefix}disconnect` ou le bouton ci-dessous pour la terminer.",
        color=discord.Color.green()
    )
    view = CloseConn(bot, ctx.author)
    if isinstance(ctx, commands.Context):
        return await ctx.reply(embed=em, view=view)
    return await ctx.response.edit_message(embed=em, view=view)


class StartConn(discord.ui.View):
    def __init__(self, bot: commands.Bot, author: Union[discord.User, discord.Member]):
        if isinstance(author, discord.Member):
            author = author._user
        self.bot = bot
        self.author = author
        super().__init__()

    async def interaction_check(self, interaction: discord.Interaction):
        return (interaction.user == self.author)

    @discord.ui.button(label="Démarrer une connexion", row=0)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await connect_check(self.bot, interaction)
        self.stop()


class CloseConn(discord.ui.View):
    def __init__(self, bot: commands.Bot, author: Union[discord.User, discord.Member]):
        if isinstance(author, discord.Member):
            author = author._user
        self.bot = bot
        self.author = author
        super().__init__()

    async def interaction_check(self, interaction: discord.Interaction):
        return (interaction.user == self.author)

    @discord.ui.button(label="Terminer la connexion", row=0)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await disconnect_check(self.bot, interaction)
        self.stop()
    


class DisplayMe(discord.ui.View):
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
        view = DeleteMessage(self.bot, interaction.user)
        self.embed.color = discord.Color.red()
        await interaction.response.edit_message(content=None, embed=self.embed, view=view)
        self.stop()
    

class DeleteMessage(discord.ui.View):
    def __init__(self, bot: commands.Bot, author: Union[discord.User, discord.Member]):
        if isinstance(author, discord.Member):
            author = author._user
        self.bot = bot
        self.author = author
        super().__init__()

    async def interaction_check(self, interaction: discord.Interaction):
        return (interaction.user == self.author)

    @discord.ui.button(label="Supprimer le message", row=0, style=discord.ButtonStyle.danger)
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
            return await ctx.reply(content=f"{ctx.author.mention}, je ne peux pas vous envoyer de message privé.", view=DisplayMe(self.bot, ctx.author, embed))
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
    
    @is_staff()
    @commands.hybrid_command(name="connect", description="Démarrer une connexion", aliases=["c", "conn"], with_app_command=True)
    async def check(self, ctx: commands.Context):
        await connect_check(self.bot, ctx)
    
    @is_staff()
    @commands.hybrid_command(name="disconnect", description="Terminer une connexion", aliases=["dc", "deco"], with_app_command=True)
    async def check(self, ctx: commands.Context):
        await disconnect_check(self.bot, ctx)
    
    @is_staff()
    @commands.hybrid_command(name="leaderboard", description="Voir le classement des connexions", with_app_command=True, aliases=["lb"])
    async def leaderboard(self, ctx: commands.Context):
        q = self.db.get.leaderboard()
        desc = "\n".join([f"{i+1}. <@{j[0]}> - {j[1]} connexion{tl.pl(j[1])}" for i, j in enumerate(q)])
        embed = discord.Embed(
            title="Classement des connexions",
            description=desc,
            color=discord.Color.blurple()
        )
        await ctx.reply(embed=embed)

    


async def setup(bot: commands.Bot):
    await bot.add_cog(Connexions(bot))
