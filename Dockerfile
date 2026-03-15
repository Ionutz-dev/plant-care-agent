# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY config/ ./config/
COPY prompts/ ./prompts/
COPY models/ ./models/
COPY schemas/ ./schemas/
COPY agents/ ./agents/
COPY utils/ ./utils/
COPY api/ ./api/
COPY frontend/ ./frontend/
COPY scripts/ ./scripts/
COPY main.py .
COPY .env .

# Copy vector store database
COPY lancedb/ ./lancedb/

# Create directory for model checkpoints if not exists
RUN mkdir -p models/checkpoints

# Expose ports
EXPOSE 8000 8501

# Default command (can be overridden in docker-compose)
CMD ["python", "main.py"]