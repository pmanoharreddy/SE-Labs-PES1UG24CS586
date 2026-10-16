# Reflection

**1. Which issues were the easiest and which were the hardest to fix?**

The Flake8 findings were the easiest: all four (E225, E303, E261, E231) were whitespace changes that took seconds and could not break anything. The naming and docstring warnings from Pylint were also easy, only repetitive, since every function had to be renamed consistently along with its calls in `main()`. The hardest was the `os.system` shell-injection issue (Bandit B605, High). Simply swapping to `subprocess` was not enough, because Bandit still flags `subprocess` (B404/B603), so I had to validate the email address, use a fixed binary path, avoid `shell=True`, pass the file through `stdin`, and justify the remaining `# nosec` markers. Replacing pickle with JSON was the second hardest, as JSON turns integer keys into strings, so `load_tasks` had to convert them back to keep the program working.

**2. Did the tools report any false positives, or did you disagree with any of them?**

Mostly no, but a couple of Bandit Low findings were of limited value. B311 (`random.choice`) is really about cryptographic use, and picking a to-do suggestion is not security-sensitive; I switched to `secrets.choice` anyway because it costs nothing. Similarly, B404 and B603 flag every use of `subprocess` even after the input has been validated and the shell removed, so I suppressed them with `# nosec` and a written reason. The `import pickle` warning (B403) was a duplicate of the more serious B301 finding. The tools also missed a few things I found by reading the code: `random.choice` would crash with an `IndexError` on an empty list, and `main()` ran on import. Static analysis helps, but does not replace reading the code.

**3. How could static analysis be integrated into a real development workflow?**

I would run all three tools automatically so problems are caught before they are merged: a pre-commit hook for Flake8 (fast, local feedback), and a CI pipeline (for example GitHub Actions) that runs Pylint with a minimum score threshold and Bandit with a fail-on-medium/high setting on every pull request. A shared configuration file (`.pylintrc`, `setup.cfg`/`.flake8`, `bandit.yaml`) would keep rules consistent across the team, and any `# nosec` or `# pylint: disable` should need a written justification and reviewer approval so warnings are not silenced casually.

**4. What tangible improvements did you see in code quality, readability, and security?**

Pylint went from 5.09/10 to 10.00/10, Bandit from 4 findings (1 High, 1 Medium, 2 Low) to none, and Flake8 from 4 findings to none. Security improved the most: the command-injection hole and the unsafe pickle deserialisation are gone. Readability improved through consistent snake_case names, docstrings on the module and every function, and a clear `return None` in `find_task`. Maintainability improved too: the mutable default argument no longer leaks state between calls, the module can be imported without side effects, and the empty-list crash is handled. I also re-ran the program after each commit to confirm the behaviour stayed the same.
