import discord
from discord.ext import commands
from discord import app_commands
from typing import Union, Optional

from tools import tools as tl
from tools.database import Database
from tools.checks import is_fonda





class Manage(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.db: Database = bot.database
    
    @is_fonda()
    @commands.hybrid_command(name="add", description="Ajouter une ou plusieurs connexion(s) à un membre", with_app_command=True, usage="add [membre] [quantite]")
    @app_commands.describe(member="Membre à qui ajouter des connexions", quantite="Nombre de connexions à ajouter")
    async def add(self, ctx: commands.Context, member: Union[discord.Member, discord.User], quantite: int):
        dont_have_q = False
        try:
            past_q = self.db.get.nb_connexions(member.id)
        except:
            dont_have_q = True
            past_q = 0
        
        new_q = past_q + quantite
        if dont_have_q:
            self.db.update.add_user(member.id, new_q)
        else:
            self.db.update.user(member.id, {"connexions": new_q})

        desc = f"Le membre {member.mention} a maintenant {new_q} connexion{tl.pl(new_q)}."
        desc += f"\n\nAnciennes connexions : {past_q}"
        if dont_have_q:
            desc += f"\n\nInfo : Ce membre n'avait aucune connexion."
        
        embed = discord.Embed(
            title="Ajout de connexion",
            description=desc,
            color=discord.Color.green()
        )
        await ctx.reply(embed=embed)
    
    @is_fonda()
    @commands.hybrid_command(name="remove", description="Retirer une ou plusieurs connexion(s) à un membre", with_app_command=True, usage="remove [membre] [quantite]", aliases=["rm"])
    @app_commands.describe(member="Membre à qui retirer des connexions", quantite="Nombre de connexions à retirer")
    async def remove(self, ctx: commands.Context, member: Union[discord.Member, discord.User], quantite: int):
        dont_have_q = False
        try:
            past_q = self.db.get.nb_connexions(member.id)
        except:
            dont_have_q = True
            past_q = 0
        
        new_q = past_q - quantite
        if new_q < 0:
            new_q = 0

        if dont_have_q:
            self.db.update.add_user(member.id, new_q)
        else:
            self.db.update.user(member.id, {"connexions": new_q})

        desc = f"Le membre {member.mention} a maintenant {new_q} connexion{tl.pl(new_q)}."
        desc += f"\n\nAnciennes connexions : {past_q}"
        if dont_have_q:
            desc += f"\n\nInfo : Ce membre n'avait aucune connexion."
        
        embed = discord.Embed(
            title="Retrait de connexion",
            description=desc,
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)
    
    @is_fonda()
    @commands.hybrid_command(name="reset", description="Réinitialiser le nombre de connexions d'un membre", with_app_command=True, usage="reset [membre]", aliases=["rst"])
    @app_commands.describe(member="Membre à qui réinitialiser les connexions")
    async def reset(self, ctx: commands.Context, member: Union[discord.Member, discord.User]):
        try:
            past_q = self.db.get.nb_connexions(member.id)
        except:
            past_q = 0
        self.db.update.user(member.id, {"connexions": 0})
        desc = f"Le membre {member.mention} n'a maintenant plus aucune connexion."
        desc += f"\n\nAnciennes connexions : {past_q}"
        embed = discord.Embed(
            title="Réinitialisation des connexions",
            description=desc,
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)
    
    @is_fonda()
    @commands.hybrid_command(name="delete", description="Supprimer un staff", with_app_command=True, usage="delete [membre]", aliases=["del"])
    @app_commands.describe(member="Membre à supprimer")
    async def delete(self, ctx: commands.Context, member: Union[discord.Member, discord.User]):
        self.db.delete.user(member.id)
        cant_delete_role = False
        try:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, id=self.bot.configs["staff_role"]))
        except discord.Forbidden:
            cant_delete_role = True
            pass
        desc = f"Le membre {member.mention} n'est maintenant plus un membre du staff et ses connexions ont été supprimées."
        if cant_delete_role:
            desc += f"\n\nInfo : je n'ai pas pu lui retirer son rôle de staff parce que mon rôle n'est pas assez haut."
        embed = discord.Embed(
            title="Suppression d'un membre",
            description=desc,
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)
    


async def setup(bot: commands.Bot):
    await bot.add_cog(Manage(bot))
