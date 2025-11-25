FROM python:3.11-slim-bookworm

# Install system dependencies required for docling and opencv
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md .gitignore ./
COPY src ./src

# Install dependencies
# We install directly since we are in a container
RUN pip install --no-cache-dir .

# Create a non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Entry point
ENTRYPOINT ["mcp-semantic-pdf-reader"]
