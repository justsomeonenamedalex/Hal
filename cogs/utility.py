import discord
from discord.ext import commands
import time


class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Functions

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog <Utility.py> is online. {time.time()}")

    # Commands

    @commands.command()
    @commands.is_owner()
    async def scrape(self, ctx):
        messages = []
        async for message in ctx.channel.history(limit=5000):
            messages.append(message.content)

        messages = [i for i in messages if i != ""]

        with open("scrape.txt", "w+") as file:
            file.write("\n".join(messages))
        await ctx.send(f"Scraped {len(messages)} messages.")


def setup(client):
    client.add_cog(Utility(client))
