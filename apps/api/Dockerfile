FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD sh -c "uv run alembic upgrade head && uv run python scripts/bootstrap_admin.py && uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
