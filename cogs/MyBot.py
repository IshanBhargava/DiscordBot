import asyncio
import logging
import time

from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

messages = joined = 0

channels: dict = {}


class MyBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Logged in as {self.client.user}")
        print(f"Logged in as {self.client.user}")
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

    # @tasks.loop(hours=1)
    async def update_stats(self):
        await self.client.wait_until_ready()
        global messages, joined

        while not self.client.is_closed():
            try:
                with open("stats.txt", "a") as f:
                    f.write(f"""Time: {time.ctime()}, Messages: {messages}, Members Joined: {joined}\n""")

                messages = 0
                joined = 0
                await asyncio.sleep(3600)
            except Exception as e:
                print(e)
                await asyncio.sleep(3600)


def setup(client):
    bot = MyBot(client)
    client.add_cog(bot)
    client.loop.create_task(bot.update_stats())
