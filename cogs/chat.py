import discord
from discord.ext import commands
import time
from chat_bot import chatBot


class Chat(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.bot = chatBot("emma.txt")

    # Functions

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog <Chat.py> is online. {time.time()}")

    # Commands
    @commands.command(aliases=["chat"])
    async def _chat(self, ctx, *, phrase):
        response = self.bot.response(phrase)
        await ctx.send(response)

    @commands.command()
    @commands.is_owner()
    async def train(self, ctx, *, file):
        self.bot = chatBot(file)

    @commands.command()
    async def model(self, ctx):
        await ctx.send(self.bot.model)


def setup(client):
    client.add_cog(Chat(client))
