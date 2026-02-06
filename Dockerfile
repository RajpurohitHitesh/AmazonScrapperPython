# Amazon Scraper API - Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Default envs
ENV API_HOST=0.0.0.0 \
    API_PORT=5000 \
    DEBUG_MODE=False

EXPOSE 5000

CMD ["python", "api_server.py"]
