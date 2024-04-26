import json
import os
from typing import Callable, TypeVar

from discord import app_commands
from discord.ext import commands

import tools.database as db

T = TypeVar("T")


def is_owner() -> Callable[[T], T]:
    """This is a custom check to see if the user is an owner of the bot.
    """

    async def predicate(context: commands.Context) -> bool:
        with open(f"configs.json", encoding="utf-8") as file:
            data = json.load(file)
        if context.author.id not in data["owners"]:
            raise commands.NotOwner
        return True

    return commands.check(predicate)


# commands.guild_only + app_commands.guild_only
def guild_only() -> Callable[[T], T]:
    """
    This is a custom check to see if the command is executed in a guild.
    """

    async def predicate(context: commands.Context) -> bool:
        if context.guild is None:
            raise commands.NoPrivateMessage
        return True

    return commands.check(predicate)

# commands.dm_only + app_commands.dm_only
def dm_only() -> Callable[[T], T]:
    """
    This is a custom check to see if the command is executed in a DM.
    """

    async def predicate(context: commands.Context) -> bool:
        if context.guild is not None:
            raise commands.PrivateMessageOnly
        return True

    return commands.check(predicate)


def has_permissions(**permissions) -> Callable[[T], T]:
    """
    This is a custom check to see if the user executing the command has the required permissions.
    """

    async def predicate(context: commands.Context) -> bool:
        if not context.guild:
            raise commands.NoPrivateMessage
        
        if not permissions:
            return True
        
        # Check if user is owner
        if context.author.id in context.bot.owner_ids:
            return True
        
        if context.guild.owner == context.author:
            return True
        
        if context.author.guild_permissions.administrator:
            return True
        
        user_permissions = context.channel.permissions_for(context.author)
        bot_permissions = context.channel.permissions_for(context.me)

        user_missing = [perm for perm in permissions if not getattr(user_permissions, perm)]
        bot_missing = [perm for perm in permissions if not getattr(bot_permissions, perm)]

        if user_missing:
            raise commands.MissingPermissions(user_missing)

        if bot_missing:
            raise commands.BotMissingPermissions(bot_missing)

        return True

    return commands.check(predicate)


def is_fonda() -> Callable[[T], T]:
    """This is a custom check to see if the user is a founder of the server.
    """

    async def predicate(context: commands.Context) -> bool:
        with open(f"configs.json") as file:
            data = json.load(file)
        
        if context.author.get_role(data["fonda_role"]) is None:
            raise commands.MissingRole(data["fonda_role"])
        return True

    return commands.check(predicate)


def is_a3() -> Callable[[T], T]:
    """This is a custom check to see if the user is an A3 staff member.
    """

    async def predicate(context: commands.Context) -> bool:
        with open(f"configs.json") as file:
            data = json.load(file)
        
        if context.author.get_role(data["a3_role"]) is None and context.author.get_role(data["fonda_role"]) is None:
            raise commands.MissingRole(data["a3_role"])
        return True

    return commands.check(predicate)

def is_staff() -> Callable[[T], T]:
    """This is a custom check to see if the user is a staff member.
    """

    async def predicate(context: commands.Context) -> bool:
        with open(f"configs.json") as file:
            data = json.load(file)
        
        if context.author.get_role(data["staff_role"]) is None and context.author.get_role(data["a3_role"]) is None and context.author.get_role(data["fonda_role"]) is None:
            raise commands.MissingRole(data["staff_role"])
        return True

    return commands.check(predicate)