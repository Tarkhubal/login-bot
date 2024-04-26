import discord
from discord.ext import commands
from discord import app_commands
from typing import Union, Optional

from tools import tools as tl
from tools.database import Database
from tools.checks import is_staff, is_a3


async def disconnect_check(bot: commands.Bot, ctx: Union[commands.Context, discord.Interaction]):
    author = ctx.author if isinstance(ctx, commands.Context) else ctx.user
    if author.id not in bot.connexions or bot.connexions[author.id] is False:
        em = discord.Embed(
            title="Aucune connexion en cours",
            description=f"Vous n'avez pas de connexion en cours.\n\nUtilisez `/connect`, `{bot.command_prefix}connect` ou le bouton ci-dessous pour en démarrer une.",
            color=discord.Color.red()
        )
    else:
        past_q = bot.database.get.nb_connexions(author.id)
        bot.database.update.user(author.id, {"connexions": past_q + 1})
        bot.connexions[author.id] = False
        em = discord.Embed(
            title="Connexion terminée",
            description=f"Votre connexion a été terminée avec succès.\n\nUtilisez `/connect`, `{bot.command_prefix}connect` ou le bouton ci-dessous pour en démarrer une nouvelle.",
            color=discord.Color.green()
        )

    view = StartConn(bot, author)
    if isinstance(ctx, commands.Context):
        return await ctx.reply(embed=em, view=view)
    return await ctx.response.edit_message(embed=em, view=view)

async def connect_check(bot: commands.Bot, ctx: Union[commands.Context, discord.Interaction]):
    author = ctx.author if isinstance(ctx, commands.Context) else ctx.user
    if author.id in bot.connexions and bot.connexions[author.id] is True:
        em = discord.Embed(
            title="Connexion en cours",
            description=f"Vous avez déjà une connexion en cours.\n\nUtilisez `/disconnect`, `{bot.command_prefix}disconnect` ou le bouton ci-dessous pour la terminer.",
            color=discord.Color.red()
        )
    else:
        bot.connexions[author.id] = True
        em = discord.Embed(
            title="Connexion démarrée",
            description=f"Vous avez démarré une connexion.\n\nUtilisez `/disconnect`, `{bot.command_prefix}disconnect` ou le bouton ci-dessous pour la terminer.",
            color=discord.Color.green()
        )
    
    view = CloseConn(bot, author)
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
    @commands.hybrid_command(name="me", description="Voir son nombre de connexions", with_app_command=True, usage="me")
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
    @commands.hybrid_command(name="check", description="Voir le nombre de connexions d'un membre", with_app_command=True, usage="check [membre]", aliases=["ch"])
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
    @commands.hybrid_command(name="connect", description="Démarrer une connexion", aliases=["c", "conn"], with_app_command=True, usage="connect")
    async def connect(self, ctx: commands.Context):
        await connect_check(self.bot, ctx)
    
    @is_staff()
    @commands.hybrid_command(name="disconnect", description="Terminer une connexion", aliases=["dc", "deco", "d"], with_app_command=True, usage="disconnect")
    async def disconnect(self, ctx: commands.Context):
        await disconnect_check(self.bot, ctx)
    
    @is_a3()
    @commands.hybrid_command(name="view", description="Voir le classement des connexions", with_app_command=True, aliases=["lb", "leaderboard"], usage="view")
    async def leaderboard(self, ctx: commands.Context):
        q = self.db.get.leaderboard()

        chunk_in = 10
        chunked = tl.chunk_list(q, chunk_in)
        descs = []
        for i, chunk in enumerate(chunked):
            desc = ""
            for j, user in enumerate(chunk):
                desc += f"`{i * chunk_in + j + 1}.` {self.bot.get_user(user[0]).mention} - {user[1]} connexion{tl.pl(user[1])}\n"
            descs.append(desc)
        embed = discord.Embed(
            title="Classement des connexions",
            description=descs[0],
            color=discord.Color.blurple()
        )
        descs = [discord.Embed(title="Classement des connexions", description=desc, color=discord.Color.blurple()) for desc in descs]
        nav_view = tl.navigation_view(ctx.author, descs, embeded=True, bot=self.bot, complex=True)
        await ctx.reply(embed=embed, view=nav_view)

    


async def setup(bot: commands.Bot):
    await bot.add_cog(Connexions(bot))
