FROM python:latest

WORKDIR /code

COPY pyproject.toml /code/
COPY uv.lock /code/

RUN pip install uv
RUN uv sync --no-group dev

COPY /SWARDEN /code/
