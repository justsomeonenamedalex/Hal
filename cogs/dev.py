import discord
from discord.ext import commands
import time
import json

class Dev(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Functions

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog <Dev.py> is online. {time.time()}")

    # Commands

    @commands.is_owner()
    @commands.command()
    async def load(self, ctx, extension: str):
        """Loads a cog"""
        try:
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} loaded.")

        except commands.NoEntryPointError as e:
            # Runs if the cog has no entry point
            # Not sure if I need this but I might as well cover everything
            await ctx.send(f"Extension {e.name} has no entry point.")

        except commands.ExtensionFailed as e:
            # Runs if there is an error in the code
            await ctx.send(f"Failed to load extension {e.name}, due to a code error:\n`{e.original}`")

        except commands.ExtensionAlreadyLoaded as e:
            await ctx.send(f"Extension {e.name} is already loaded.")

        except commands.ExtensionNotFound as e:
            await ctx.send(f"Extension {e.name} not found.")

    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx, extension: str):
        """Unloads a cog"""
        try:
            self.client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} unloaded.")

        except commands.ExtensionFailed as e:
            # Runs if there is an error in the code
            await ctx.send(f"Failed to unload extension {e.name}, due to a code error:\n`{e.original}`")

        except commands.ExtensionNotLoaded as e:
            await ctx.send(f"Extension {e.name} is not loaded")

        except commands.ExtensionNotFound as e:
            await ctx.send(f"Extension {e.name} not found.")

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx, extension: str):
        """Unloads, then loads a cog"""
        # Unload the cog
        try:
            self.client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} unloaded.")

        except commands.ExtensionFailed as e:
            await ctx.send(f"Failed to unload extension {e.name}, due to a code error:\n`{e.original}`")

        except commands.ExtensionNotLoaded as e:
            await ctx.send(f"Extension {e.name} is not loaded")

        except commands.ExtensionNotFound as e:
            await ctx.send(f"Extension {e.name} not found.")

        # Load the cog
        try:
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} loaded.")

        except commands.NoEntryPointError as e:
            # Not sure if I need this but I might as well cover everything
            await ctx.send(f"Extension {e.name} has no entry point.")

        except commands.ExtensionFailed as e:
            await ctx.send(f"Failed to load extension {e.name}, due to a code error:\n`{e.original}`")

    @commands.is_owner()
    @commands.command()
    async def activity(self, ctx, *, text):
        """Sets the activity of the bot manually"""
        # TODO: Make this override the cycling status somehow
        await self.client.change_presence(activity=discord.Game(text))
        await ctx.send(f"Activity set to {text}")

    @commands.is_owner()
    @commands.command(aliases=["shutdown", "off"])
    async def goodnight(self, ctx):
        """Safely shuts down the bot"""
        await ctx.send("Bot shutting down")

        await self.client.change_presence(status=discord.Status.offline)
        await self.client.logout()

    @commands.command()
    @commands.is_owner()
    async def invite(self, ctx):
        with open("../config.json") as file:
            config = json.load(file)
        invite = config["INVITE"]
        await ctx.send(invite)



def setup(client):
    client.add_cog(Dev(client))
