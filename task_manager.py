
import json
from pathlib import Path

TASKS_FILE = Path(__file__).with_name("tasks.json")

try:
    with open(TASKS_FILE, "r") as file:
        data = json.load(file)

    if (
        isinstance(data["pending_tasks"], list)
        and isinstance(data["completed_tasks"], list)
    ):
        work = data["pending_tasks"]
        completed_tasks = data["completed_tasks"]

    else:
        print("Invalid task data. Starting with empty lists.")
        work = []
        completed_tasks = []

except FileNotFoundError:
    work = []
    completed_tasks = []

except (json.JSONDecodeError, KeyError, TypeError):
    print("Invalid or corrupted JSON file. Starting with empty lists.")
    work = []
    completed_tasks = []


def save_tasks():
    data = {
        "pending_tasks": work,
        "completed_tasks": completed_tasks
    }

    with open(TASKS_FILE, "w") as file:
        json.dump(data, file, indent=4)
