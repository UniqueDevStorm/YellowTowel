from discord.ext import commands

from __main__ import YellowTowel


class Listener(commands.Cog):
    def __init__(self, bot: YellowTowel):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.CheckFailure):
            print(ctx.author)


def setup(bot: YellowTowel):
    bot.add_cog(Listener(bot))
