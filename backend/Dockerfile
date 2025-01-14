FROM python:3.12-slim

WORKDIR /backend

RUN pip install poetry

COPY . /backend/

RUN poetry install

ENV POETRY_VIRTUALENVS_CREATE=false

CMD ["poetry", "run", "start"]