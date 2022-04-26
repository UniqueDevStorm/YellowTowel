from discord.ext import commands
from discord import Embed, Member
from discord.ext.commands.context import Context

from __main__ import YellowTowel
from utils import getDatabase, saveDatabase

from typing import Optional


def isRegister():
    data = getDatabase()

    def predicate(ctx: Context):
        return True if data.get(str(ctx.author.id)) else False

    return commands.check(predicate)


class Economy(commands.Cog):
    def __init__(self, bot: YellowTowel):
        self.bot = bot
        self.shopItems = {
            "도둑능력+1": 2000,
            "도둑방어+1": 1000,
            "돌멩이": 20,
            "포도": 150,
            "참외": 190,
            "담배": 300,
            "양철북": 2000,
            "도끼": 4500,
            "망루": 9999,
            "복권": 500,
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
            database[str(ctx.author.id)] = {"money": "100", "items": {}}
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

    @commands.command(name="인벤", aliases=["인벤토리", "inventory"])
    @isRegister()
    async def inventory(self, ctx: Context, target: Optional[Member]):
        if target is None:
            target = ctx.author
        items = (getDatabase())[str(target.id)]["items"]
        return await ctx.reply(
            embed=Embed(
                title=f"{target.display_name} 의 인벤토리",
                description="\n".join(
                    [
                        f"=도둑질 {f'성공률+{items[_]}' if _ == '도둑능력+1' else f'방어율+{items[_]}'}%"
                        if _ == "도둑방어+1" or _ == "도둑능력+1"
                        else f"{_}×{items[_]}개"
                        for _ in items
                    ]
                ),
            )
        )

    @commands.command(name="구매")
    @commands.guild_only()
    @isRegister()
    async def buy(self, ctx: Context, item: str, count: int = 1):
        if count <= 0:
            return
        if self.shopItems.get(item) is None:
            return
        database = getDatabase()
        if int(database[str(ctx.author.id)]["money"]) < self.shopItems[item] * count:
            return await ctx.reply("잔액이 부족합니다 (`.돈`으로 확인)")
        if database[str(ctx.author.id)]["items"].get(item) is None:
            database[str(ctx.author.id)]["items"][item] = 0
        database[str(ctx.author.id)]["items"][item] += count
        database[str(ctx.author.id)]["money"] = str(
            int(database[str(ctx.author.id)]["money"]) - self.shopItems[item] * count
        )
        if saveDatabase(database):
            return await ctx.reply(
                f"{ctx.message.author.display_name}님이 ({item} x{count}개)을(를) [{self.shopItems[item] * int(count)} SGD"
                "]에 구매하였습니다",
            )


def setup(bot: YellowTowel):
    bot.add_cog(Economy(bot))
