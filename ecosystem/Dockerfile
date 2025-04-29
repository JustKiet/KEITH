FROM python:3.13-slim

WORKDIR /ecosystem

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies using uv
RUN pip install duckduckgo-search httpx loguru "mcp[cli]" openai pydantic requests unstructured

# Copy the rest of the project files
COPY . /ecosystem/

EXPOSE 8088

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/ecosystem

CMD ["python", "main.py"]