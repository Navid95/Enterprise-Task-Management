FROM python:3.12-slim AS builder

ENV POETRY_HOME="/etc/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/etc/poetry/bin:$PATH"

RUN apt-get update && apt install curl -y
WORKDIR /app
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --no-root

FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

RUN groupadd -r etm && useradd --no-log-init -r -g etm etm
COPY . .
RUN chown -R etm:etm /app
USER etm

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]