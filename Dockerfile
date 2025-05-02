# Purpose: Defines the Docker container setup for the FX Trading Bot.
# Ensures consistent development and deployment environments.

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for ta-lib, MetaTrader5, and other libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libta-lib0 \
    libta-lib-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables (placeholder, to be overridden in docker-compose.yml)
ENV PYTHONUNBUFFERED=1
ENV MT5_LOGIN=""
ENV MT5_PASSWORD=""
ENV MT5_SERVER=""

# Expose port for potential UI or API (optional, can be adjusted)
EXPOSE 8000

# Define entrypoint to run the bot
ENTRYPOINT ["python", "src/main.py"]