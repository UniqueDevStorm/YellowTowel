from discord.ext import commands
from discord import Embed, Color, Member
from discord.ext.commands.context import Context

from __main__ import YellowTowel
from utils import getDatabase, saveDatabase


def isRegister():
    data = getDatabase()

    async def predicate(ctx: Context):
        if data["users"].get(str(ctx.author.id)) is None:
            await ctx.reply(embed=Embed(title="등록부터 하쇼 (.시작)", color=Color.red()))
            return False
        return True

    return commands.check(predicate)


def channelOnly():
    return commands.check(
        lambda ctx: ctx.channel.id in [955264379421622345, 967932672234094612]
    )


class Economy(commands.Cog):
    def __init__(self, bot: YellowTowel):
        self.bot = bot
        self.defaultUserStructure = {
            "money": 100,
            "maxMoney": 1000,
            "earnings": 0,
            "credit": 1,
            "loan": {},
            "stats": {"도둑성공률": 20, "도둑방어율": 0, "인구": 20},
            "items": {},
            "workers": {"고쓰카이": 10, "보조배달": 0},
        }

    @commands.command(name="도움말", aliases=["help", "도움"])
    @channelOnly()
    async def _help(self, ctx: Context):
        embed = Embed(
            title="명령어 모음",
            description="[.시작] : 등록\n[.상점] : 상점확인\n[.ㄷ] : 돈 확인\n[.구매 <이름> <개수>]: 상점에서 구매\n[.한강] : 초기화\n[.사채 <대상> <금액> "
            "<이자율> <시간>] : 사채대출주기\n[.대출 <금액>] : 1금융권 대출(이자율 5%, 기간 10분)\n[.사채갚기 <대상> <금액>] : 사채갚기\n[.대출갚기 "
            "<금액>] : 대출갚기\n[.송금 <대상> <금액>] : 돈보내기\n",
            color=Color.red(),
        )
        await ctx.channel.send(embed=embed)

    @commands.command(name="시작")
    @channelOnly()
    async def start(self, ctx: Context):
        database = getDatabase()
        if database["users"].get(str(ctx.author.id)) is None:
            try:
                database["users"][str(ctx.author.id)] = self.defaultUserStructure
            except KeyError:
                database["users"] = {}
                database["users"][str(ctx.author.id)] = self.defaultUserStructure
            if saveDatabase(database):
                return await ctx.reply(embed=Embed(description="등록했습죠"))
            return await ctx.reply("문제가 생긴거 같쇼..")
        return await ctx.reply("이미 등록했습죠")

    @commands.command(name="한강")
    @isRegister()
    @channelOnly()
    async def hanRiver(self, ctx: Context):
        database = getDatabase()
        database["users"].pop(str(ctx.author.id))
        saveDatabase(database)
        return await ctx.reply(
            embed=Embed(
                title=f"{ctx.author.display_name} 님이 한강에 뛰어들었습니다 (.시작으로 재시작)",
                color=Color.red(),
            )
        )

    @commands.command(name="돈", aliases=["money", "ㄷ"])
    @isRegister()
    async def money(self, ctx: Context):
        database = getDatabase()
        userId = str(ctx.author.id)

        txt = f"돈 [{database['users'][userId]['money']}/{database['users'][userId]['maxMoney']} SGD]\n"
        loanNum = 0
        for i in database["users"][userId]["loan"]:
            loanNum += 1
            if database["users"][userId]["loan"][i]["amount"] > 0:
                txt += f"대출#{loanNum} - [{i}: -{database['users'][userId]['loan'][i]['amount']}]\n"
        txt += f"신용등급 [{database['users'][userId]['credit']} 등급]\n\n" f"[노동자]\n"
        database["users"][userId]["earnings"] = 0
        for i in database["users"][userId]["workers"]:
            if (
                i in database["shop"]["workers"]
                and database["users"][userId]["workers"][i] > 0
            ):
                txt += f"[{i} x {database['users'][userId]['workers'][i]}]: +{database['users'][userId]['workers'][i] * database['shop']['workers'][i][1]} SGD 수입\n"
                database["users"][userId]["earnings"] += (
                    database["users"][userId]["workers"][i]
                    * database["shop"]["workers"][i][1]
                )
        txt += f"총수입: [{database['users'][userId]['earnings']} SGD]\n인구: [{sum([database['users'][userId]['workers'][_] for _ in database['users'][userId]['workers']])}/{database['users'][userId]['stats']['인구']}]"
        txt += f"\n\n[아이템]\n"
        for i in database["users"][userId]["items"]:
            if (
                i in database["shop"]["items"]
                and database["users"][userId]["items"][i] > 0
            ):
                txt += f"[{i} x {database['users'][userId]['items'][i]}]: {database['shop']['items'][i][1]}\n"
        txt += f"\n[스탯]\n"
        for i in database["users"][userId]["stats"]:
            if i in database["shop"]["stats"] and i != "돈한계":
                txt += f"{i}: +{database['users'][userId]['stats'][i]}\n"
        return await ctx.reply(
            embed=Embed(
                title=f"{ctx.author.display_name}의 자산",
                description=txt,
                color=Color.gold(),
            )
        )

    @commands.command(name="송금")
    @isRegister()
    @channelOnly()
    async def send(self, ctx: Context, user: Member, amount: int):
        database = getDatabase()
        userId = str(ctx.author.id)
        if amount > 0:
            if int(database["users"][userId]["money"]) >= amount:
                if database["users"].get(str(user.id)):
                    database["users"][userId]["money"] -= amount
                    database["users"][str(user.id)]["money"] += amount

                    saveDatabase(database)
                    return await ctx.reply(
                        embed=Embed(
                            title="송금 완료",
                            description=f"{ctx.author.display_name} ---> {user.display_name}\n[{amount} SGD 송금]",
                            color=Color.gold(),
                        )
                    )
                return await ctx.reply("대상이 존재하지 않습니다")
            return await ctx.reply("보낼 돈이 없습니다.")
        return await ctx.reply("보내실 돈이 양수여야 합니다.")

    @commands.command(name="상점")
    @channelOnly()
    async def shop(self, ctx: Context):
        database = getDatabase()
        txt = "💎 노동자\n"
        for i in database["shop"]["workers"]:
            txt += f"[{i} : 수입 +{database['shop']['workers'][i][1]} SGD] -- [{database['shop']['workers'][i][0]} SGD]\n"
        txt += "\n💎 아이템\n"
        for i in database["shop"]["items"]:
            txt += f"[{i} : {database['shop']['items'][i][1]}] -- [{database['shop']['items'][i][0]} SGD]\n"
        txt += "\n💎 스탯\n"
        for i in database["shop"]["stats"]:
            txt += f"[{i}] -- [{database['shop']['stats'][i][0]} SGD]\n"
        return await ctx.reply(
            embed=Embed(title="상점", description=txt, color=Color.blurple())
        )

    @commands.command(name="해고")
    @isRegister()
    @channelOnly()
    async def _fire(self, ctx: Context, item: str, amount: int = 1):
        database = getDatabase()
        userId = str(ctx.author.id)
        if amount > 0:
            if item in database['users'][userId]['workers']:
                if database['users'][userId]['workers'][item] >= amount:
                    database['users'][userId]['workers'][item] -= amount
                    return await ctx.reply(
                        embed=Embed(
                            title="해고 완료",
                            description=f"[{item} x {amount}명] 해고고",
                            color=Color.red(),
                        ))
                return await ctx.reply("보유 수량이 부족합니다.")
            return await ctx.reply("노동자가 존재하지 않습니다.")
        return await ctx.reply("구매하려는 개수가 양수여야 합니다.")

    @commands.command(name="구매")
    @isRegister()
    @channelOnly()
    async def buy(self, ctx: Context, item: str, amount: int = 1):
        database = getDatabase()
        userId = str(ctx.author.id)
        if amount > 0:
            for category in database["shop"]:
                for name in database["shop"][category]:
                    if name == item:
                        if category == "workers":
                            if (
                                database["users"][userId]["stats"]["인구"]
                                < amount + database["users"][userId]["workers"][item]
                            ):
                                return await ctx.reply(
                                    "구매 가능 인구를 초과했습죠.\n(.상점)에서 인구를 추가 구매하쇼"
                                )
                        if (
                            database["users"][userId]["money"]
                            >= amount * database["shop"][category][name][0]
                        ):
                            database["users"][userId]["money"] -= (
                                amount * database["shop"][category][name][0]
                            )
                            database["users"][userId][category][item] += amount
                            saveDatabase(database)
                            return await ctx.reply(
                                embed=Embed(
                                    title="구매 완료",
                                    description=f"{ctx.author.display_name}\n{item} x {amount} [{amount * database['shop'][category][name][0]} SGD]구매",
                                    color=Color.gold(),
                                )
                            )
                        return await ctx.reply("돈이 부족합니다.")
            return await ctx.reply("아이템이 존재하지 않습니다.")
        return await ctx.reply("구매하려는 개수가 양수여야 합니다.")


def setup(bot: YellowTowel):
    bot.add_cog(Economy(bot))
