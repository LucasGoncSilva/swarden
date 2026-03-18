FROM python:3.14-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl libpq-dev && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock Cargo.toml Cargo.lock ./
COPY SWARDEN/rust ./SWARDEN/rust

RUN uv sync --frozen --no-install-project

COPY . .

RUN uv run python SWARDEN/manage.py collectstatic --noinput --clear

FROM python:3.14-slim-bookworm AS prod

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && rm -rf /var/lib/apt/lists/*

RUN groupadd --system django && useradd --system --gid django django

WORKDIR /app/SWARDEN

COPY --from=builder --chown=django:django /app/.venv /app/.venv
COPY --from=builder --chown=django:django /app /app

ENV PATH="/app/.venv/bin:/app/SWARDEN:${PATH}" \
    PYTHONPATH="/app/SWARDEN" \
    DJANGO_SETTINGS_MODULE="CORE.settings" \
    PYTHONUNBUFFERED=1

USER django

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "-c", "gunicorn.conf.py", "CORE.wsgi:application"]
# CMD ["python", "server.py"]
