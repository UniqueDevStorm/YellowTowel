import json
from typing import Dict, Union
import logging


def createLogger() -> logging.Logger:
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    fileHandler = logging.FileHandler(
        filename="discord.log", encoding="utf-8", mode="w"
    )
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    return logger


def getDatabase() -> Dict[str, dict]:
    with open("./database.towel", "r", encoding="utf8") as f:
        data = f.read()
    return json.loads(data)


def saveDatabase(data: dict):
    with open("./database.towel", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True
