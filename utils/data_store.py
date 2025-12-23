import json
from pathlib import Path

DATA_PATH = Path("data/user_data.json")


def load_data():
    if not DATA_PATH.exists():
        return {"users": {}}

    with open(DATA_PATH, "r") as f:
        return json.load(f)


def save_data(data):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)
