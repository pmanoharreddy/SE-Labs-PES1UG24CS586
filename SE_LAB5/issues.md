# Issues Found by Static Analysis — `todo_manager.py`

Line numbers refer to the **original** file (before fixes). Reports are in `reports/before/` and `reports/after/`.

| Tool | Before | After |
| ---- | ------ | ----- |
| Pylint | 5.09 / 10 | **10.00 / 10** |
| Bandit | 1 High, 1 Medium, 2 Low | **0 issues** |
| Flake8 | 4 issues | **0 issues** |

## Issue table (high and medium severity first)

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| OS command injection via `os.system` (Bandit B605, **High**) | Security | 57 | `remindByEmail` builds a shell command by concatenating the caller-supplied `address`. An input like `a@b.com; rm -rf ~` would run arbitrary commands. | Validate `address` with a strict email regex, then call `subprocess.run([...], shell=False)` with a fixed argument list and feed `tasks.json` through `stdin` instead of shell redirection. |
| Unsafe deserialisation with `pickle.load` (Bandit B301, **Medium**) | Security | 47 | Unpickling can execute arbitrary code if `tasks.pkl` is tampered with. | Replaced pickle with JSON in `save_tasks` / `load_tasks`; integer task ids are restored on load because JSON keys are strings. |
| Mutable default argument `labels=[]` (Pylint W0102) | Bug | 11 | The same list object is shared across every call, so labels leak between tasks. | Default changed to `None`; a fresh list is created inside the function and stored on the task. |
| `import pickle` (Bandit B403, Low) | Security | 3 | Flags use of the pickle module. | Removed with the pickle-to-JSON change. |
| `random.choice` (Bandit B311, Low) | Security | 70 | `random` is not a cryptographically secure generator. | Switched to `secrets.choice`. |
| Latent crash on empty list | Bug | 70 | `random.choice([])` raises `IndexError` once every task is complete (not tool-reported; found while reviewing). | Added an `if pending:` guard with a friendly message. |
| Inconsistent return statements (Pylint R1710) | Bug / Style | 33-36 | `findTask` returns an id on a match but falls off the end (implicit `None`) otherwise. | Added an explicit `return None` and documented it. |
| `open()` without encoding (Pylint W1514) | Bug | 51 | Behaviour depends on the platform's default encoding. | Added `encoding="utf-8"` to every `open()` call in text mode. |
| camelCase names (Pylint C0103) | Style | 11, 12, 19, 27, 33, 34, 40, 45, 50, 55 | `addTask`, `taskId`, `fileName`, etc. violate PEP 8 snake_case. | Renamed to `add_task`, `task_id`, `file_name`, `complete_task`, `pending_tasks`, `find_task`, `save_tasks`, `load_tasks`, `export_json`, `remind_by_email`. |
| Missing docstrings (Pylint C0114 / C0116) | Style | 1, 11, 19, 27, 33, 40, 45, 50, 55, 60 | Module and nine functions have no documentation. | Added a module docstring and a docstring on every function. |
| `main()` runs on import | Design | 79 | Importing the module executes the demo and writes files. | Wrapped in `if __name__ == "__main__":`. |
| E225 missing whitespace around operator (Flake8) | Style | 12 | `taskId=len(tasks) + 1` | `task_id = len(tasks) + 1` |
| E303 too many blank lines (Flake8) | Style | 40 | Three blank lines before `saveTasks`. | Reduced to two. |
| E261 two spaces before inline comment (Flake8) | Style | 69 | `)) # returns None silently` | Two spaces before `#`. |
| E231 missing whitespace after `,` (Flake8) | Style | 74 | `"...from file:",len(restored)` | Added a space after the comma. |

## Notes on suppressed warnings

Two Bandit Low findings are intentionally suppressed with `# nosec` and a justification, because they are false positives once the code is safe:

- **B404** (`import subprocess`) — the module is imported but only used with a fixed argument list and no shell.
- **B603** (`subprocess.run`) — the executable path is hard-coded, the only variable argument (`address`) is validated against an email regex before use, and `shell=False`.

## Behaviour change to be aware of

`save_tasks` now writes `tasks_saved.json` instead of `tasks.pkl` (pickle was removed). Output of the demo is otherwise identical.
