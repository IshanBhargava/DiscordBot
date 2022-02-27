from discord.ext import commands


@commands.command()
async def hello(message, arg):
    print("inside hello")
    await message.send('Hello {0}.'.format(arg))


def setup(bot):
    bot.add_command(hello)
