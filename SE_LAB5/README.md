# Lab 5: Static Code Analysis — To-Do List & Task Manager

**Your file:** `todo_manager.py`

Follow the lab handout for the full instructions.

## About the program

A task manager. It adds tasks with a priority, marks them complete, lists pending tasks in priority order, searches by keyword, suggests a task to do next, and saves tasks to JSON files (`tasks_saved.json` and `tasks.json`; the original version used `tasks.pkl`, which was replaced because pickle is unsafe).

The code works, but only just. It has quality, style and security problems of the kind Pylint, Flake8 and Bandit are built to find.

## What to do

1. **Run it first** and read the output carefully:

   ```
   python todo_manager.py
   ```

   It runs a short demonstration and needs no input. Note what it prints, so you can check that it still behaves the same after your fixes.

2. **Install the tools:**

   ```
   python -m pip install pylint bandit flake8
   ```

3. **Run the analysis and save the reports:**

   ```
   python -m pylint todo_manager.py > pylint_report.txt
   python -m bandit -r todo_manager.py > bandit_report.txt
   python -m flake8 todo_manager.py > flake8_report.txt
   ```

4. **Document the issues** in `issues.md` using this table (at least 4 rows, high and medium severity first):

   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | ...   | ...  | ...     | ...         | ...          |

5. **Fix the code.** Fix at least 4 of the issues you documented, then rerun all three tools to confirm they are gone. Repeat until you are satisfied. The program should still do its job when you are done.

6. **Reflect.** Answer the four reflection questions from the handout in `reflection.md`.

## Deliverables

- `todo_manager.py`: your cleaned version, with at least 4 issues fixed.
- `issues.md`: the completed issue table.
- `reflection.md`: your answers to the reflection questions.

**Target:** aim for a Pylint score above 9.5 on your final file. A perfect 10.00/10 is very good.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.

---

## My Submission

### Results

| Tool | Before | After |
| ---- | ------ | ----- |
| Pylint | 5.09 / 10 | **10.00 / 10** |
| Bandit | 1 High, 1 Medium, 2 Low | **0 issues** |
| Flake8 | 4 issues | **0 issues** |

### What was fixed

- **Bandit:** shell command injection in `remindByEmail` (B605), unsafe `pickle` (B301/B403) and `random.choice` (B311).
- **Flake8:** E225, E303, E261, E231.
- **Pylint:** snake_case names, missing docstrings, mutable default argument, inconsistent return, missing file encoding, and `main()` running on import.

### Files

| File | Purpose |
| ---- | ------- |
| `todo_manager.py` | Cleaned and fixed program |
| `issues.md` | Table of all issues found and how each was fixed |
| `Lab5_Issue_Table.docx` | The same issue table as a Word document |
| `reflection.md` | Answers to the reflection questions |
| `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt` | Final reports (after fixes) |
| `reports/before/` | Reports on the original code |
| `reports/after/` | Reports on the fixed code |

### Commits

1. Original code, README and baseline reports
2. Bandit fixes
3. Flake8 fixes
4. Pylint fixes
5. After-fix reports, `issues.md` and `reflection.md`
6. Update README, `issues.md` and `reflection.md`, and add the issue table as a Word document

### How to run and re-check

```
python todo_manager.py
python -m pylint todo_manager.py
python -m bandit -r todo_manager.py
python -m flake8 todo_manager.py
```

Note: two Bandit Low warnings (B404, B603) are suppressed with `# nosec` and a written justification; see `issues.md`.
