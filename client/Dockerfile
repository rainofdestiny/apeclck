# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app
COPY pyproject.toml ./
RUN uv sync --frozen --no-install-project

COPY . .
RUN uv sync --frozen

ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "python", "main.py"]
