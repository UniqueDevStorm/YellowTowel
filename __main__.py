from discord.ext import commands
from discord import Intents

import os
from dotenv import load_dotenv

from utils import createLogger

load_dotenv(verbose=True)


class YellowTowel(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv("PREFIX")),
            intents=Intents.all(),
            help_command=None,
        )
        logger = createLogger()
        for extension in os.listdir("./exts"):
            if extension.endswith(".py"):
                self.load_extension(f"exts.{extension[:-3]}")
                logger.info(f"Loaded {extension}")
        self.load_extension("jishaku")
        self.owner_ids = [299895531701010442, 754848549019320441]
        logger.info("Loaded jishaku")


if __name__ == "__main__":
    YellowTowel().run(os.getenv("TOKEN"))
