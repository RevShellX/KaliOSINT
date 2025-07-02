# KaliOSINT Dockerfile
# Multi-stage build for optimized image size

# Build stage
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    nmap \
    whois \
    dnsutils \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    KALIOSINT_HOME=/opt/kaliosint

# Create non-root user
RUN useradd --create-home --shell /bin/bash kaliosint

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    nmap \
    whois \
    dnsutils \
    curl \
    wget \
    tor \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set working directory
WORKDIR $KALIOSINT_HOME

# Copy application files
COPY src/ src/
COPY config/ config/
COPY scripts/ scripts/
COPY main.py .
COPY requirements.txt .

# Create directories for user data
RUN mkdir -p /home/kaliosint/.kaliosint/{config,results,logs,cache} && \
    chown -R kaliosint:kaliosint /home/kaliosint/.kaliosint && \
    chown -R kaliosint:kaliosint $KALIOSINT_HOME

# Switch to non-root user
USER kaliosint

# Copy default configuration
RUN cp config/default_config.json /home/kaliosint/.kaliosint/config/config.json && \
    cp config/api_keys.json.template /home/kaliosint/.kaliosint/config/api_keys.json

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.core.main import KaliOSINT; print('OK')" || exit 1

# Expose port (if needed for future web interface)
EXPOSE 8080

# Default command
CMD ["python", "main.py"]

# Labels for metadata
LABEL maintainer="KaliOSINT Team" \
    version="1.0.0" \
    description="Advanced OSINT Terminal Tool for Kali Linux" \
    license="MIT"
