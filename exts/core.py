from discord.ext import commands
from discord import Message, Embed
from discord.ext.commands.context import Context

from __main__ import YellowTowel

import asyncio


class Core(commands.Cog):
    def __init__(self, bot: YellowTowel):
        self.bot = bot

    @commands.command(name="뭐해")
    async def whatDoYouDoing(self, ctx: Context):
        return await ctx.reply("신문배달 합죠")

    @commands.command(name="센세")
    async def sense(self, ctx: Context):
        return await ctx.reply("센세이 히, 오하요 고자이마쓰카 히히 아메가 후리마쓰 유키가 후리마쓰카 히히")

    @commands.command(name="그런데")
    async def sakewa(self, ctx: Context):
        return await ctx.reply(
            "사······ 케······ 와 나······ 미다카 다메이······ 키······ 카······"
        )

    @commands.command(name="참외")
    async def orientalMelon(self, ctx: Context):
        return await ctx.reply("선생님 잡수시라굽쇼")

    @commands.command(name="포도")
    async def grape(self, ctx: Context):
        message: Message = await ctx.reply("선생님 잡수라고 사 왔습죠")
        await asyncio.sleep(1)
        return await message.edit(content="센세이 히, 오하요 고자이마쓰카 히히 아메가 후리마쓰 유키가 후리마쓰카 히히")

    @commands.command(name="달밤")
    async def dalbam(self, ctx: Context):
        return await ctx.reply("달밤은 그에게도 유감한 듯하였다.")

    @commands.command(name="아이고난1")
    async def aigonan(self, ctx: Context):
        return await ctx.reply("아이고난2")

    @commands.command(name="여자야?")
    async def areYouWoman(self, ctx: Context):
        return await ctx.reply("개소리하지마십죠")

    @commands.command(name="넌")
    async def you(self, ctx: Context):
        return await ctx.reply("수건입죠")

    @commands.command(name="몇살이야")
    async def howOldAreYou(self, ctx: Context):
        return await ctx.reply("그게 말입니다요.. 3살인가.. 14살인가.. 15살인가.. 92..6..53..58..")

    @commands.command(name="뭐할수있어")
    async def whatCanYouDo(self, ctx: Context):
        return await ctx.reply("아, 방학될 때까지 차미 장사도 하굽쇼, 가을부턴 군밤장사..")

    @commands.command(name="취미가뭐야")
    async def whatIsYourHobby(self, ctx: Context):
        return await ctx.reply("신문배달입죠")

    @commands.command(name="도움말", aliases=["help", "도움"])
    async def _help(self, ctx: Context):
        return await ctx.reply(
            embed=Embed(
                title=f"명령어",
                description=".시작: 계좌 개설. 100SGD 획득 (인당 1회)\n"
                ".돈 : 잔액 확인\n "
                ".송금 <대상> <금액>: 송금하기 (10% 세율)\n"
                ".부자순위: 서버 전체 자산 내림차순\n"
                ".그지순위: 서버 전체 자산 오름차순\n"
                ".상점: 구매가능 목록\n"
                ".인벤: 인벤토리\n"
                ".올인: 전체 돈 2배 또는 0 (50%)",
            )
        )


def setup(bot: YellowTowel):
    bot.add_cog(Core(bot))
