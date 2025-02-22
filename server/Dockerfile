FROM python:3.12-slim

WORKDIR /backend

RUN pip install poetry

COPY . /backend/

RUN poetry install

ENV POETRY_VIRTUALENVS_CREATE=false

RUN chmod +x /backend/entrypoint.sh

CMD ["/backend/entrypoint.sh"]