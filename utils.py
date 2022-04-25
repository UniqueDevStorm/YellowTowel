import json
from typing import Dict


def getDatabase() -> Dict[str, Dict[str, int]]:
    with open('./database.towel', 'r', encoding='utf8') as f:
        data = f.read()
    return json.loads(data)


def saveDatabase(data: Dict[str, Dict[str, int]]):
    with open('./database.towel', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True
