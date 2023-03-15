FROM python:3.10-slim

WORKDIR /app
RUN pip install "poetry==1.4.0"

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . /app/
