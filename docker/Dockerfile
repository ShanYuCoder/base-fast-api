FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml README.md ./
COPY src ./src

RUN uv pip install --system -e ".[dev]" 2>/dev/null || uv pip install --system fastapi "uvicorn[standard]" pydantic pydantic-settings httpx typer jinja2 pyyaml pytest pytest-asyncio

ENV PYTHONPATH=/app/src
EXPOSE 4000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4000", "--app-dir", "src"]
