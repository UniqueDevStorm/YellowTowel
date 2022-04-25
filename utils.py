import json


def getDatabase() -> dict:
    with open("./database.towel", "r", encoding="utf8") as f:
        data = f.read()
    return json.loads(data)


def saveDatabase(data: dict):
    with open("./database.towel", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True
