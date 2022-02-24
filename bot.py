import discord

intents = discord.Intents.default()
intents.members = True


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0]


token = read_token()

client = discord.Client(intents=intents)

channel_ids: dict = {
    "server-id": 946301558545592341,
    "bot-commands": 946356930388041748,
    "bot-logs": 946392782912761859
}

channels = ['general', 'bot-commands', 'bot-logs']


@client.event
async def on_member_join(member):
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send(f"""Welcome to the server {member.mention}""")


@client.event
async def on_message(message):
    serverid = client.get_guild(channel_ids["server-id"])

    if message.author == client.user:
        return
    if message.content:
        print("{0.author} sent a message - {0.content}".format(message))

    if message.content.startswith("!") and str(message.channel) == "bot-commands":
        if message.content in ["!hello"]:
            await message.channel.send("Hi")

        if message.content in ["!users", "!user"]:
            await message.channel.send("Number of Members: {0.member_count}".format(serverid))

        if message.content in ["!commands", "!command"]:
            await message.channel.send("Commands: \n !hello \n !users")

    else:
        await client.get_channel(channel_ids["bot-logs"]).send(f"""User: {message.author} tried to execute command \'{message.content}\' in {message.channel}""")
        await message.channel.send(f"""{message.author.mention} the bot commands can only be executed in {client.get_channel(channel_ids["bot-commands"]).mention} channel""")

client.run(token)


