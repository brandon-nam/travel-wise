# Overview of packages/subdirectories
## ai_provider
- This entails an AI provider, with an abstract method `prompt(query: str, params: dict) -> str`.
- We provide an example in the form of `OpenAIProvider`. 
- If we ever wanted to swap out to `ClaudeProvider`, for e.g., it would be easy.

## fs_access
- This entails file system access, with relevant methods related to getting relevant file paths, opening and writing new files.
- For example, `LocalFSAccess` shows you how to define access for local files.
- If we ever wanted to swap out to another file system, such as S3/GCS, it would be easy.

## handlers
- This entails steps in our transformation pipeline. We have two base classes currently, `BaseHandler` and `BaseAIHandler` (which relies on AI prompts)
- We have example handlers shown for our Reddit pipeline.

## transformers
- contains abstract `transform()` method to be called from the main entrypoint.
- We instantiate a transformer with an instance of `FSAccess`, and declare the `chain: list[BaseHandler]` property.
- For example, look at `RedditTransformer`
- We follow the **Chain of Responsibility** design pattern here; it is compulsory to have a chain of handlers and we can easily remove, add or swap the ordering of the handlers.
- Additionally if we ever wanted to obtain data from another source, say, Facebook, it would be easy to extend by creating another transformer.

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
- In the root directory of this project, run `poetry install` to install the required dependencies (e.g. `flask`, `black`, etc.)
- Finally, `poetry run start` will run the code locally.
