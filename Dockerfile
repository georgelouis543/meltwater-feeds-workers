FROM --platform=linux/amd64 python:3.12-slim

# Install uv (for dependency management)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy application into container
WORKDIR /worker
COPY . /worker

# Install dependencies into virtual environment
RUN uv sync --frozen --no-cache

# Default environment variables (can be overridden in ECS)
ENV CELERY_LOG_LEVEL=info

# Default command — can be overridden in ECS Task Definition
CMD ["/worker/.venv/bin/celery", "-A", "worker.celery_app.celery_app", "worker", "-l", "info"]
