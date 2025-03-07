# Development Guide
## Git Workflow
- To contribute, first checkout to a separate branch i.e. `git checkout -b <branch_name>`
- Make your code changes, then use `poetry run black .` and `poetry run ruff check --fix` to format and lint the code.
- Use `git add` and `git commit` to record your code changes.
- Use `git push -u origin <branch_name>` to push your changes to GitHub, then create a pull request to the `main` branch.

## Adding dependencies to project
- We are using `poetry` to manage our dependencies. This consists of two files
  - `pyproject.toml`
  - `poetry.lock`
- Don't edit these two files manually. If you wish to add a dependency, for example `pandas`, run `poetry add pandas`
- After adding one or more dependencies, you will notice changes in the two files above. You must commit and push these changes.

# Running The Code
## How to run with CLI
- Ensure you have Python on your system, version `>=3.12`
- If you do not have [poetry](https://python-poetry.org/), run `pip install poetry`
- In the root directory of this project, run `poetry install` to install the required dependencies.
- Populate `.env` file (see [here](https://www.reddit.com/prefs/apps) to generate Reddit API key/secret)
- Use `poetry run start` to run the collector code ([TODO]: Currently writes to local)