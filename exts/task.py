from discord.ext import commands, tasks

from __main__ import YellowTowel
from utils import getDatabase, saveDatabase


class Task(commands.Cog):
    def __init__(self, bot: YellowTowel):
        self.bot = bot
        self.workersWorking.start()

    @tasks.loop(seconds=5)
    async def workersWorking(self):
        database = getDatabase()
        role = {}
        for worker in database["shop"]["workers"]:
            role[worker] = database["shop"]["workers"][worker][1]
        for user in database["users"]:
            for worker in database["users"][user]["workers"]:
                if (
                    database["users"][user]["money"]
                    + role[worker] * database["users"][user]["workers"][worker]
                    > database["users"][user]["maxMoney"]
                ):
                    continue
                database["users"][user]["money"] += (
                    role[worker] * database["users"][user]["workers"][worker]
                )
        saveDatabase(database)


def setup(bot: YellowTowel):
    bot.add_cog(Task(bot))
