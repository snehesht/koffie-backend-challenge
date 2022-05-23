FROM python:3.10.4-slim-buster

RUN pip install "poetry"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . /app

EXPOSE 8000

ENTRYPOINT [ "python3", "/app/app/main.py" ]