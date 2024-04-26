import discord
import json
import os

from tools.database import Database
import tools.tools as tl
from tools.configs import Configs

from discord.ext import commands, tasks
from tools.terminal_print import TerminalColors as c



try:
    os.system('cls')
except:
    os.system('clear')

configs: Configs = Configs("configs.json")

TOKEN = configs.get("DEVTOKEN") if configs.get("dev_mode_is_activated") else configs.get("TOKEN")

if not os.path.exists(configs.get("database_name")):
    open(configs.get("database_name"), "w", encoding="utf-8").close()
    print(f"{c.vert}Created database file{c.reset}")


class Bot(commands.Bot):
    def __init__(self, configs: Configs):
        self.configs = configs
        self.database = Database(self.configs.get("database_name"))
        self.columns = json.load(open("db_columns.json", "r", encoding="utf-8"))

        for table in self.columns:
            self.database.create_table(table, self.columns[table])
        
        super().__init__(command_prefix = self.configs["prefix"], intents = discord.Intents.all(), help_command=None)

    async def startup(self):
        await bot.wait_until_ready()
        # If you want to define specific guilds, pass a discord object with id (currently, this is global)
        await bot.tree.sync(guild=None)
        print(f'{c.vert}Sucessfully synced applications commands')
        print(f'{c.bleu}Hello ! I\'m connected as {c.violet}{bot.user} ({bot.user.id}){c.reset}, with Discord.py version {c.jaune}{discord.__version__}{c.bleu} and SQLite3.\nHappy hack !{c.reset}')

    async def setup_hook(self):
        print(f"{c.bleu}Loading cogs...{c.reset}")
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    print(f"⨮ {c.vert}Loaded {filename}{c.reset}")
                except Exception as e:
                    print(f"⨵ {c.rouge}Failed to load {filename}{c.reset}")
                    print(f"⨵ {c.rouge}       [ERROR] {e}{c.reset}")
        self.loop.create_task(self.startup())
        print(f"{c.bleu}Cogs loaded\n{len(bot.all_commands)} {tl.pl(bot.all_commands, 'command')}{c.reset}")

bot = Bot(configs)

# Base bot using discord.py and sqlite3 made by thomas0535. Deleting this copyright is illegal. Commercial use is illegal without written permission of thomas0535. You can use this code for your own bot but you must credit me.
# Deleting or modifying this copyright will not make you the author of this and it's illegal.
# https://tarkhubal.github.io | thb5309@gmail.com

@bot.event
async def on_ready():
    # print(bot.all_commands)
    await bot.wait_until_ready()
    await bot.change_presence(activity=discord.Activity(name=f"gérer Pelican", type=discord.ActivityType.playing))

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot or message.author.id == bot.user.id:
        return
    
    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        await message.add_reaction("✌️")
    
    if message.content == bot.user.mention:
        await message.reply(f"Mon préfix est `{bot.command_prefix}`. Pour voir mes commandes, tape `{bot.command_prefix}help`.")
    
    await bot.process_commands(message)
    


@bot.command(name="ping", aliases=[], usage="ping", help="Affiche le ping du bot", description="Affiche le ping du bot")
async def ping(ctx: commands.Context) -> None:
    ping = round(bot.latency * 1000)
    print(f"Pong ! {ping}ms")
    await ctx.reply(f"Pong ! {ping}ms")


bot.run(TOKEN)
