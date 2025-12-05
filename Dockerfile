# ---------- Stage 1: builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

# Install system deps: cron + tzdata
RUN apt-get update && apt-get install -y \
    cron tzdata curl \
 && rm -rf /var/lib/apt/lists/*

# Copy Python deps from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . /app

# Create volume mount points
RUN mkdir -p /data /cron \
 && chmod 755 /data /cron

# Install cron job
COPY cron/cronfile /etc/cron.d/app-cron
RUN chmod 0644 /etc/cron.d/app-cron \
 && crontab /etc/cron.d/app-cron

# Expose API port
EXPOSE 8080

# Start cron and FastAPI
CMD service cron start && \
    uvicorn app:app --host 0.0.0.0 --port 8080
    # Create volume mount points
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Install cron job for logging 2FA codes
COPY cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

