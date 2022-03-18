import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs import BotCommands, MyBot

load_dotenv(dotenv_path=Path('./discord.env'))
token = os.getenv('token')

client = commands.Bot(command_prefix="!", intents=discord.Intents().all())

cogs = [BotCommands, MyBot]
for cog in cogs:
    cog.setup(client)

client.run(token)
