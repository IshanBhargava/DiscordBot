import random

from discord.ext import commands

import ApiService as api

channel_ids: dict = {
    "server": 946301558545592341,
    "bot-logs": 946392782912761859,
    "general": 946301559040507927
}


def is_mod(ctx) -> bool:
    for role in ctx.author.roles:
        if role.name == "Mod":
            return True
    else:
        return False


class BotCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        help="Greets the user"
    )
    async def hello(self, ctx):
        await ctx.trigger_typing()
        await ctx.send(f"Hello! {ctx.author.mention}")

    @commands.command(
        help="Syntax: !draw <count> <channel name> <msg ID>"
    )
    async def draw(self, ctx, *args):
        if str(ctx.channel) != 'bot-logs':
            await ctx.send(
                f"This command cannot be executed in this channel. Try in {ctx.guild.get_channel(channel_ids['bot-logs']).mention}")
        else:
            if is_mod(ctx):
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
                await self.client.get_channel(channel_ids["bot-logs"]).send(
                    f"""User: {ctx.author} tried to execute an unauthorized command \'{ctx.content}\' in {ctx.channel}""")

    @commands.command(
        help="Tells a joke"
    )
    async def joke(self, ctx):
        await ctx.trigger_typing()
        await ctx.send(api.joke())


def setup(client):
    client.add_cog(BotCommands(client))
