# How to run with CLI
- Ensure you have Python on your system, version `>=3.12`
- If you do not have [poetry](https://python-poetry.org/), run `pip install poetry`
- In the root directory of this project, run `poetry install` to install the required dependencies (e.g. `flask`, `black`, etc.)
- Finally, `poetry run start` will start the server locally.
- Open your browser and verify that `localhost:3203` displays "Hello World!"

# How to run with Docker
- Build the docker image using `docker build -t <your tag> .`
- Run the docker image using `docker run -p 3203:3203 <your tag>`
  - Port is currently hardcoded as 3203, `-p` forwards it to your local
- Open your browser and verify that `localhost:3203` displays "Hello World!"