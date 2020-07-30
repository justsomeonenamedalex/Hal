import json
import os
import discord
from discord.ext import commands, tasks

with open("config.json") as file:
    # Import the config settings
    config = json.load(file)

bot = commands.Bot(command_prefix=config["COMMAND_PREFIX"])


def load_cogs(dir_path: str):
    for filename in os.listdir(dir_path):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{filename[:-3]}")
            except commands.ExtensionFailed as e:
                print(f"Failed to load {e.name}:\n{e.original}")


@bot.event
async def on_ready():
    """This function runs when the bot starts up"""
    activity = config["DEFAULT_ACTIVITY_MESSAGE"]
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(activity))


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """Handles errors when commands are used"""

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"You are missing the follow argument: `{error.param}`")
    else:
        print(error)

# Load the cogs and run the bot
if config["LOAD_COGS"]:
    load_cogs("./cogs")
BOT_TOKEN = config["BOT_TOKEN"]
bot.run(BOT_TOKEN)
