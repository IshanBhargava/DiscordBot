import random

from discord.ext import commands

import ApiService as api
from bot import client

channel_ids: dict = {
    "server": 946301558545592341,
    "bot-logs": 946392782912761859,
    "general": 946301559040507927
}


@commands.command()
async def hello(ctx):
    await ctx.trigger_typing()
    await ctx.send(f"Hello! {ctx.author.mention}")


@commands.command()
async def draw(ctx, *args):
    ismod = False
    for role in ctx.author.roles:
        if role.name == "Mod":
            ismod = True
            break

    if ismod:
        draw_count = int(args[0])
        try:
            msg = await ctx.guild.get_channel(channel_ids[args[1]]).fetch_message(args[2])
        except:
            await ctx.trigger_typing()
            msg = None

        if msg is not None:
            reacted_users = set()

            for reaction in msg.reactions:
                async for user in reaction.users():
                    reacted_users.add(f"""{user.name}#{user.discriminator}""")
            if len(reacted_users) == 0:
                await ctx.send(f"Oops! Nobody reacted")
            elif draw_count > len(reacted_users):
                await ctx.send(f"users: {', '.join(user for user in reacted_users)}")
            else:
                await ctx.send(f"users: {', '.join(user for user in random.sample(reacted_users, draw_count))}")
        else:
            await ctx.send(
                f"Oops! It seems that the message does not exist. Please check the channel name and message id.")
    else:
        await ctx.send(f"""{ctx.author.mention} you are not authorized to use this command""")
        await client.get_channel(channel_ids["bot-logs"]).send(
            f"""User: {ctx.author} tried to execute an unauthorized command \'{ctx.content}\' in {ctx.channel}""")


@commands.command()
async def joke(ctx):
    await ctx.trigger_typing()
    await ctx.send(api.joke())


def setup(bot):
    bot.add_command(hello)
    bot.add_command(draw)
    bot.add_command(joke)
