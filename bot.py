import discord
import time
import asyncio

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

channels = ['general', 'bot-commands', 'bot-logs']
commands = ["!hello", "!users"]


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"""Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n""")

            messages = 0
            joined = 0

            await asyncio.sleep(60)
        except Exception as e:
            print(e)
            await asyncio.sleep(60)


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

    if message.content:
        print("{0.author} sent a message - {0.content}".format(message))

    if message.content in ["!help", "!commands"]:
        embed = discord.Embed(title="Help on DeadBot", description="Some Bot commands")
        embed.add_field(name="!hello", value="Greets the user")
        embed.add_field(name="!users", value="Returns number of users")
        if str(message.channel) != "bot-commands":
            embed.set_footer(text=f"""Use these commands in {client.get_channel(channel_ids["bot-commands"]).name} channel""")
        await message.channel.send(content=None, embed=embed)

    if message.content.startswith("!") and message.content in commands:
        if str(message.channel) == "bot-commands":
            if message.content == "!hello":
                await message.channel.send("Hi")

            if message.content == "!users":
                await message.channel.send("Number of Members: {0.member_count}".format(serverid))

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

