import discord


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0]


token = read_token()

client = discord.Client()

@client.event
async def on_message(message):
    serverid = client.get_guild(946301558545592341)
    channels = ['bot-commands']


    if str(message.channel) in channels:
        if message.author == client.user:
            return
        else:
            if message.content:
                print("{0.author} sent a message - {0.content}".format(message))

            if message.content in ["!hello"]:
                await message.channel.send("Hi")

            if message.content in ["!users", "!user"]:
                await message.channel.send("Number of Members: {0.member_count}".format(serverid))

            if message.content in ["!commands", "!command"]:
                await message.channel.send("Commands: \n !hello \n !users")



client.run(token)


