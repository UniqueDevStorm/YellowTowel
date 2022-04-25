from discord.ext import commands
from discord import Intents, Game

import os
from dotenv import load_dotenv

load_dotenv(verbose=True)


class YellowTowel(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix="//", intents=Intents.all(), help_command=None)
        for extension in os.listdir("./exts"):
            if extension.endswith(".py"):
                self.load_extension(f"exts.{extension[:-3]}")
                print(f"Loaded {extension}")
        self.load_extension("jishaku")
        self.owner_ids = [299895531701010442]
        print("Loaded jishaku")

    async def on_ready(self):
        await self.change_presence(activity=Game(name="신문 배달"))
        print(f"Logged in as {self.user}")


if __name__ == "__main__":
    YellowTowel().run(os.getenv("TOKEN"))
