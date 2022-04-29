from discord import Game
from discord.ext import commands

from __main__ import YellowTowel


class Listener(commands.Cog):
    def __init__(self, bot: YellowTowel):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.CheckFailure):
            return
        else:
            print(error)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=Game(name="신문 배달 (.도움말)"))
        print(f"Logged in as {self.bot.user}")


def setup(bot: YellowTowel):
    bot.add_cog(Listener(bot))
