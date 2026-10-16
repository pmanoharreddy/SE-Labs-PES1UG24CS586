# Reflection

**1. Which issues were the easiest and which were the hardest to fix?**

The easiest were the Flake8 issues. There were only four (E225, E303, E261, E231) and all of them were just spacing or blank-line mistakes, so fixing them could not break the program. Renaming functions to snake_case and adding docstrings for Pylint was also easy, just repetitive, because I had to change every function name and every place it was called.

The hardest was the security problem in `remindByEmail` (Bandit B605, High). It used `os.system` and joined the email address straight into a shell command, so someone could type extra commands after the address. Just switching to `subprocess` was not enough, because Bandit also warns about `subprocess` (B404 and B603). I had to check the email address with a pattern, give the full path of the mail program, turn the shell off, and pass the file as input instead of using `<`. Replacing `pickle` with JSON was the second hardest. JSON turns the number keys (1, 2, 3) into text, so `load_tasks` has to turn them back into numbers or the program breaks.

**2. Did the tools report any false positives, or did you disagree with any?**

Mostly the tools were right. A few Bandit warnings were not very useful. B311 (`random.choice`) only matters for passwords and security, and picking a to-do suggestion is not security related, but I changed it to `secrets.choice` anyway because it costs nothing. B404 and B603 still warn about `subprocess` even after the input is checked and the shell is off, so I silenced those two with `# nosec` and wrote the reason next to them. B403 (`import pickle`) was the same problem as B301, so it went away with the same fix.

The tools also missed some problems that I found by reading the code. `random.choice` would crash with an error if every task was done, and `main()` ran automatically whenever the file was imported. So the tools help a lot, but they do not replace reading the code.

**3. How could static analysis be used in a real development workflow?**

I would run the tools automatically so problems are caught before the code is merged. Flake8 can run as a pre-commit hook because it is fast. Pylint (with a minimum score) and Bandit (failing on medium or high issues) can run in a CI pipeline such as GitHub Actions on every pull request. The team should share one config file so everyone follows the same rules, and every `# nosec` or `# pylint: disable` should need a written reason that a reviewer approves, so warnings are not hidden carelessly.

**4. What improvements did you see in quality, readability and security?**

The scores show it clearly: Pylint went from 5.09/10 to 10.00/10, Bandit went from 4 issues (1 High, 1 Medium, 2 Low) to none, and Flake8 went from 4 issues to none. Security improved the most, because the command injection problem and the unsafe `pickle` loading are gone. Readability improved because the names follow one style, every function has a docstring, and `find_task` clearly returns `None` when nothing is found. The code is also more reliable now: the mutable default argument is fixed, importing the file no longer runs the demo, and the empty-list crash is handled. I ran the program after each commit to check that it still worked.
