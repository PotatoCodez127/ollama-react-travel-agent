FROM python:3.11-slim

# Enforce deterministic runtime environment variables
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=UTC

# Isolate dependency layers to optimize container cache structures
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy remaining codebase modules into the container working layer
COPY . .

# Default execution entrypoint for the autonomous ReAct engine
CMD ["python", "agent.py"]