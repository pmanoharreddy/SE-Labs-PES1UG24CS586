import json
import re
import secrets
# subprocess is only used with a fixed argument list and no shell
import subprocess  # nosec B404
from datetime import datetime

tasks = {}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
MAIL_BIN = "/usr/bin/mail"
EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def addTask(title, priority="medium", labels=[]):
    taskId = len(tasks) + 1
    labels.append(priority)
    tasks[taskId] = {"title": title, "priority": priority, "done": False,
                     "created": datetime.now().isoformat()}
    return taskId


def completeTask(taskId):
    if taskId in tasks:
        tasks[taskId]["done"] = True
        return True
    print("No task with id", taskId)
    return False


def pendingTasks():
    pending = [task for task in tasks.values() if not task["done"]]
    pending.sort(key=lambda task: PRIORITY_ORDER[task["priority"]])
    return [task["title"] for task in pending]


def findTask(keyword):
    for taskId, task in tasks.items():
        if keyword.lower() in task["title"].lower():
            return taskId


def saveTasks(fileName="tasks_saved.json"):
    with open(fileName, "w") as f:
        json.dump(tasks, f, indent=2)


def loadTasks(fileName="tasks_saved.json"):
    with open(fileName, "r") as f:
        # JSON object keys are always strings; restore the integer task ids
        return {int(key): value for key, value in json.load(f).items()}


def exportJson(fileName="tasks.json"):
    with open(fileName, "w") as f:
        json.dump(tasks, f, indent=2)


def remindByEmail(address):
    # Helper kept for the lab: not called by the demo
    if not EMAIL_PATTERN.fullmatch(address):
        raise ValueError("Invalid email address: " + repr(address))
    with open("tasks.json", "rb") as body:
        # Fixed binary path, address validated above, no shell involved
        subprocess.run(  # nosec B603
            [MAIL_BIN, "-s", "Pending tasks", address],
            stdin=body, check=True, shell=False)


def main():
    addTask("Submit lab report", "high")
    addTask("Buy groceries")
    addTask("Call plumber", "low")
    addTask("Book train tickets", "high")
    completeTask(2)
    completeTask(99)
    print("Pending tasks:", pendingTasks())
    print("Task id for 'plumber':", findTask("plumber"))
    print("Task id for 'gym':", findTask("gym"))  # returns None silently
    suggestion = secrets.choice(pendingTasks())
    print("Try this next:", suggestion)
    saveTasks()
    restored = loadTasks()
    print("Tasks restored from file:", len(restored))
    exportJson()
    print("Exported tasks to tasks.json")


main()
