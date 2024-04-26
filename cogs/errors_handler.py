import discord
import difflib

from discord.ext import commands

class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        print(f"ERROR : ```{error}``` | Message : {ctx.message} | {ctx.message.content}")
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Erreur",
                description="Vous n'avez pas la permission d'utiliser cette commande",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            command = self.bot.get_command(ctx.command.name)
            usage = command.usage
            if usage is None:
                usage = f"{ctx.prefix}{command.name} [Usage non défini]"
            
            embed = discord.Embed(
                title="Erreur",
                description=f"Vous n'avez pas renseigné tous les arguments nécessaires\nUsage : `{usage}`\n\n`[argument]` : argument obligatoire\n`<argument>` : argument facultatif",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.BadArgument) or isinstance(error, commands.BadUnionArgument):
            command = self.bot.get_command(ctx.command.name)
            usage = command.usage
            if usage is None:
                usage = f"{ctx.prefix}{command.name} [Usage non défini]"
            embed = discord.Embed(
                title="Erreur",
                description=f"Vous n'avez pas renseigné les arguments correctement\nUsage : `{usage}`\n\n`[argument]` : argument obligatoire\n`<argument>` : argument facultatif",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.TooManyArguments):
            command = self.bot.get_command(ctx.command.name)
            usage = command.usage
            if usage is None:
                usage = f"{ctx.prefix}{command.name} [Usage non défini]"
            embed = discord.Embed(
                title="Erreur",
                description=f"Vous avez renseigné trop d'arguments\nUsage : `{usage}`\n\n`[argument]` : argument obligatoire\n`<argument>` : argument facultatif",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.CommandOnCooldown):
            # Obtenir le temps restant avant de pouvoir réutiliser la commande
            hours, remainder = divmod(int(error.retry_after), 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours == 0:
                if minutes == 0:
                    time = f"{seconds} seconde{'s' if seconds > 1 else ''}"
                else:
                    time = f"{minutes} minute{'s' if minutes > 1 else ''} et {seconds} seconde{'s' if seconds > 1 else ''}"
            else:
                time = f"{hours} heure{'s' if hours > 1 else ''}, {minutes} minute{'s' if minutes > 1 else ''} et {seconds} seconde{'s' if seconds > 1 else ''}"
            embed = discord.Embed(
                title="Cooldown !",
                description="Vous devez attendre avant de pouvoir réutiliser cette commande :/\n\nTemps restant : " + time,
                color=discord.Color.red()
            )
        elif isinstance(error, commands.MaxConcurrencyReached):
            embed = discord.Embed(
                title="Erreur",
                description="Vous avez atteint le nombre maximum d'utilisation de cette commande en même temps",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="Erreur",
                description="Vous n'êtes pas le propriétaire du bot",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="Erreur",
                description="Le bot n'a pas la permission d'utiliser cette commande",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.MissingRole):
            embed = discord.Embed(
                title="Erreur",
                description="Vous n'avez pas le rôle nécessaire pour utiliser cette commande",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.RoleNotFound):
            embed = discord.Embed(
                title="Erreur",
                description="Le rôle n'a pas été trouvé",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                title="Erreur",
                description="Le membre n'a pas été trouvé",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.ChannelNotFound):
            embed = discord.Embed(
                title="Erreur",
                description=f"Le salon {error.argument} n'a pas été trouvé",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.ChannelNotReadable):
            embed = discord.Embed(
                title="Erreur",
                description="Le bot n'a pas la permission de voir ce salon",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.NSFWChannelRequired):
            embed = discord.Embed(
                title="Erreur",
                description="Cette commande ne peut être utilisée que dans un salon NSFW",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(
                title="Erreur",
                description="Cette commande est désactivée",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.CommandNotFound):
            similar_command = difflib.get_close_matches(ctx.invoked_with, [command for command in self.bot.all_commands.keys()])
            embed = discord.Embed(
                title="Erreur",
                description=f"Cette commande n'existe pas\nVous ne voulez pas dire `{similar_command[0] if similar_command != [] else '(aucune commande ressemblante trouvée)'}` ?",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.NoPrivateMessage):
            embed = discord.Embed(
                title="Oups",
                description="Vous ne pouvez pas utiliser cette commande en message privé",
                color=discord.Color.red()
            )
        elif isinstance(error, NotImplementedError):
            embed = discord.Embed(
                title="Oups",
                description="Cette commande/fonctionnalité est encore en développement, désolé :(",
                color=discord.Color.red()
            )
        else:
            print(error)
            embed = discord.Embed(
                title="Erreur",
                description=f"Une erreur est survenue, cela vient sûrement du code. Contactez le développeur du bot ({self.bot.get_user(755738381455065120).mention}) ou un administrateur du serveur",
                color=discord.Color.red()
            )
        
        
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        await ctx.send(
            embed=embed,
            view=discord.ui.View().add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.link,
                    url="https://discord.gg/Q6Zh6TMKnF",
                    label="Serveur Discord",
                    emoji="🚸"
                )
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(ErrorHandler(bot))