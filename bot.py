import asyncio
import random
import time

import discord


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0]


messages = joined = 0

token = read_token()

intents = discord.Intents().all()
client = discord.Client(intents=intents)

channel_ids: dict = {
    "server-id": 946301558545592341,
    "bot-commands": 946356930388041748,
    "bot-logs": 946392782912761859,
    "general": 946301559040507927
}
channels = []

commands_dict: {} = {
    "!hello": "Greets the user",
    "!users": "Displays number of members in server",
    "!draw": "Randomly selects users who reacted on the specified msg. Only Mods can use this."
}


@client.event
async def on_ready():
    print(client.user.name)
    for guild in client.guilds:
        for channel in guild.text_channels:
            channels.append(channel.name)


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


@client.event
async def on_member_join(member):
    global joined
    joined += 1
    await client.get_channel(channel_ids["general"]).send(f"""{member.mention} Welcome to the server!""")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    serverid = client.get_guild(channel_ids["server-id"])
    global messages
    messages += 1

    if message.content in ["!help", "!commands"]:
        embed = discord.Embed(title="Help on DeadBot", description="Some Bot commands")
        for command, use in commands_dict.items():
            embed.add_field(name=command, value=use)

        if str(message.channel) != "bot-commands":
            embed.set_footer(
                text=f"""Use these commands in {client.get_channel(channel_ids["bot-commands"]).name} channel""")
        await message.channel.send(content=None, embed=embed)

    elif message.content.startswith("!"):
        if "!draw" in message.content:
            mod_flag = False
            for role in message.author.roles:
                if role.name == "Mod":
                    mod_flag = True
                    break
            if mod_flag:
                channel = client.get_channel(message.channel.id)
                msg_id = int(message.content.split(' ')[2])
                draw_count = int(message.content.split(' ')[1])

                msg = await channel.fetch_message(msg_id)
                reacted_users = set()
                for reaction in msg.reactions:
                    async for user in reaction.users():
                        reacted_users.add(user.name)

                if draw_count > len(reacted_users):
                    await message.channel.send(f"users: {', '.join(user for user in reacted_users)}")
                else:
                    await message.channel.send(f"users: {', '.join(user for user in random.sample(reacted_users, draw_count))}")
            else:
                await message.channel.send(f"""{message.author.mention} you are not authorized to use this command""")
                await client.get_channel(channel_ids["bot-logs"]).send(f"""User: {message.author} tried to execute an unauthorized command \'{message.content}\' in {message.channel}""")

        elif str(message.channel) == "bot-commands":
            if message.content == "!hello":
                await message.channel.send("Hi")

            elif message.content == "!users":
                await message.channel.send("Number of Members: {0.member_count}".format(serverid))

            else:
                await message.channel.send(f"""{message.content} is not a valid command""")

        else:
            await client.get_channel(channel_ids["bot-logs"]).send(f"""User: {message.author} tried to execute command \'{message.content}\' in {message.channel}""")
            await message.channel.send(f"""{message.author.mention} the bot commands can only be executed in {client.get_channel(channel_ids["bot-commands"]).mention} channel""")


@client.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        if n.lower().count("deadshot"):
            last = before.nick
            if last:
                await after.edit(nick=last)
            else:
                await after.edit(nick="NO STOP THAT")


client.loop.create_task(update_stats())
client.run(token)

