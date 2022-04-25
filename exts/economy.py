from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context

from __main__ import YellowTowel
from utils import getDatabase, saveDatabase


class Economy(commands.Cog):
    def __init__(self, bot: YellowTowel):
        self.bot = bot
        self.shopItems = {
            "돌멩이": 20,
            "포도": 150,
            "참외": 190,
            "담배": 300,
            "양철북": 2000,
            "도끼": 4500,
            "망루": 9999,
            "[직업]고쓰카이": 50,
            "[직업]원배달": 400,
            "[직업]보조배달": 200,
            "[직업]신문사사장": 1000,
            "[직업]파수꾼": 5000,
            "[직업]촌장": 10000,
        }

    @commands.command(name="시작")
    async def start(self, ctx: Context):
        database = getDatabase()
        if database.get(str(ctx.author.id)) is None:
            database[str(ctx.author.id)] = {
                "money": 100,
                "items": {}
            }
            if saveDatabase(database):
                return await ctx.reply(
                    embed=Embed(description=f"{ctx.author.mention} 의 자산\n**100 SGD**")
                )
            return await ctx.reply("문제가 생긴거 같쇼..")
        return await ctx.reply("이미 했습죠")

    @commands.command(name="상점")
    async def shop(self, ctx: Context):
        return await ctx.reply(
            embed=Embed(
                title="상점",
                description="`.구매 <제품ID>로 구매`\n\n```{0}```".format(
                    "\n".join(
                        [f"{_}: [{self.shopItems[_]} SGD]" for _ in self.shopItems]
                    )
                ),
            )
        )


def setup(bot: YellowTowel):
    bot.add_cog(Economy(bot))