"""To-do list and task manager.

Adds tasks with a priority, marks them complete, lists pending tasks in
priority order, searches by keyword, suggests a task to do next and saves
tasks to JSON files.
"""
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


def add_task(title, priority="medium", labels=None):
    """Add a task and return its id.

    ``labels`` is an optional list of extra labels; the priority is always
    added as a label too. A fresh list is created on every call.
    """
    task_id = len(tasks) + 1
    labels = [] if labels is None else list(labels)
    labels.append(priority)
    tasks[task_id] = {"title": title, "priority": priority, "done": False,
                      "labels": labels,
                      "created": datetime.now().isoformat()}
    return task_id


def complete_task(task_id):
    """Mark a task as done. Return True if it exists, otherwise False."""
    if task_id in tasks:
        tasks[task_id]["done"] = True
        return True
    print("No task with id", task_id)
    return False


def pending_tasks():
    """Return titles of unfinished tasks, highest priority first."""
    pending = [task for task in tasks.values() if not task["done"]]
    pending.sort(key=lambda task: PRIORITY_ORDER[task["priority"]])
    return [task["title"] for task in pending]


def find_task(keyword):
    """Return the id of the first task whose title contains ``keyword``.

    The search ignores case. Return None if nothing matches.
    """
    for task_id, task in tasks.items():
        if keyword.lower() in task["title"].lower():
            return task_id
    return None


def save_tasks(file_name="tasks_saved.json"):
    """Save all tasks to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def load_tasks(file_name="tasks_saved.json"):
    """Load tasks from a JSON file and return them as a dict."""
    with open(file_name, "r", encoding="utf-8") as file:
        # JSON object keys are always strings; restore the integer task ids
        return {int(key): value for key, value in json.load(file).items()}


def export_json(file_name="tasks.json"):
    """Export all tasks to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def remind_by_email(address):
    """Email the exported task list to ``address``.

    Helper kept for the lab: not called by the demo.
    """
    if not EMAIL_PATTERN.fullmatch(address):
        raise ValueError("Invalid email address: " + repr(address))
    with open("tasks.json", "rb") as body:
        # Fixed binary path, address validated above, no shell involved
        subprocess.run(  # nosec B603
            [MAIL_BIN, "-s", "Pending tasks", address],
            stdin=body, check=True, shell=False)


def main():
    """Run a short demonstration of the task manager."""
    add_task("Submit lab report", "high")
    add_task("Buy groceries")
    add_task("Call plumber", "low")
    add_task("Book train tickets", "high")
    complete_task(2)
    complete_task(99)
    print("Pending tasks:", pending_tasks())
    print("Task id for 'plumber':", find_task("plumber"))
    print("Task id for 'gym':", find_task("gym"))  # returns None silently
    pending = pending_tasks()
    if pending:
        print("Try this next:", secrets.choice(pending))
    else:
        print("Nothing pending - all tasks are done!")
    save_tasks()
    restored = load_tasks()
    print("Tasks restored from file:", len(restored))
    export_json()
    print("Exported tasks to tasks.json")


if __name__ == "__main__":
    main()
