from discord import Member
from discord.ext import commands
from discord.ext.commands.context import Context

from __main__ import YellowTowel
from utils import getDatabase, saveDatabase


class Owner(commands.Cog):
    def __init__(self, bot: YellowTowel):
        self.bot = bot

    @commands.command(name="delete")
    @commands.guild_only()
    @commands.is_owner()
    async def accountDelete(self, ctx: Context, target: Member):
        data = getDatabase()
        if data.get(str(target.id)) is None:
            return
        data.pop(str(target.id))
        saveDatabase(data)
        return await ctx.message.add_reaction("✅")

    @commands.command(name="리셋", aliases=["reset"])
    @commands.guild_only()
    @commands.is_owner()
    async def reset(self, ctx: Context):
        data = getDatabase()
        data["users"] = {}
        saveDatabase(data)
        return await ctx.message.add_reaction("✅")


def setup(bot: YellowTowel):
    bot.add_cog(Owner(bot))
