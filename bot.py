import asyncio
import logging
import time

import discord
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0]


messages = joined = 0
token = read_token()

intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", intents=intents)
client.load_extension("BotCommands")

channels: dict = {}

commands_dict: {} = {
    "!hello": "Greets the user",
    "!draw": "Randomly selects users who reacted on the specified msg. Only Mods can use this.",
    "!joke": "Tells a joke"
}


class MyBot(commands.Cog):
    def __init__(self, botclient):
        self.client = botclient

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Logged in as {self.client.user}")
        for guild in self.client.guilds:
            if 'server' not in channels:
                channels['server'] = guild.id
            for channel in guild.text_channels:
                channels[channel.name] = channel.id

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        global messages
        messages += 1

    @commands.Cog.listener()
    async def on_member_join(self, member):
        global joined
        joined += 1
        await self.client.get_channel(channels["general"]).send(f"""Welcome to the server {member.mention}!""")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        n = after.nick
        if n:
            if n.lower().count("deadshot"):
                last = before.nick
                if last:
                    await after.edit(nick=last)
                else:
                    await after.edit(nick="NO CAN'T DO THAT")

    @staticmethod
    async def update_stats():
        await client.wait_until_ready()
        global messages, joined

        while not client.is_closed():
            try:
                with open("stats.txt", "a") as f:
                    f.write(f"""Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n""")

                messages = 0
                joined = 0

                await asyncio.sleep(3600)
            except Exception as e:
                print(e)
                await asyncio.sleep(3600)


client.add_cog(MyBot(client))
client.loop.create_task(MyBot.update_stats())
client.run(token)
