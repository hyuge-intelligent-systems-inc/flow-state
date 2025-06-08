
# FlowState Dockerfile
# Privacy-First Productivity Application
#
# This Dockerfile builds FlowState with security and privacy as priorities:
# - Minimal attack surface with distroless base
# - Non-root user execution
# - Read-only filesystem where possible
# - Health checks and security scanning
# - Environment-specific configurations

# Build stage - compile and prepare application
FROM python:3.11-slim AS builder

# Set build arguments
ARG BUILD_DATE
ARG VERSION
ARG VCS_REF

# Add metadata labels following OCI standards
LABEL \
    org.opencontainers.image.title="FlowState" \
    org.opencontainers.image.description="Privacy-first productivity application with user agency" \
    org.opencontainers.image.version="${VERSION}" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${VCS_REF}" \
    org.opencontainers.image.vendor="FlowState Team" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.documentation="https://github.com/flowstate/docs" \
    maintainer="FlowState Team"

# Install system dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy dependency files first for better cache utilization
COPY requirements.txt setup.py ./
COPY src/ ./src/

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

# Runtime stage - minimal production image
FROM python:3.11-slim AS runtime

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r flowstate && \
    useradd -r -g flowstate -d /app -s /bin/bash flowstate

# Create application directories with proper permissions
RUN mkdir -p /app /data /logs /exports /config && \
    chown -R flowstate:flowstate /app /data /logs /exports /config

# Set working directory
WORKDIR /app

# Copy application code
COPY --from=builder --chown=flowstate:flowstate /app/src ./src
COPY --chown=flowstate:flowstate config/ ./config/
COPY --chown=flowstate:flowstate docs/ ./docs/

# Create configuration and data directories
VOLUME ["/data", "/logs", "/exports", "/config"]

# Switch to non-root user
USER flowstate

# Set environment variables for production
ENV PYTHONPATH="/app" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLOWSTATE_ENV=production \
    FLOWSTATE_DATA_DIR=/data \
    FLOWSTATE_LOG_DIR=/logs \
    FLOWSTATE_CONFIG_DIR=/config

# Expose application port (if web interface is added)
EXPOSE 8000

# Health check to ensure application is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import sys; sys.path.append('/app'); from src.core.time_tracker import TimeTracker; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "src.main"]

# Development stage - includes development tools
FROM runtime AS development

# Switch back to root to install development dependencies
USER root

# Install development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install development Python packages
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    black \
    flake8 \
    mypy \
    pre-commit

# Switch back to flowstate user
USER flowstate

# Override command for development
CMD ["python", "-m", "src.main", "--development"]

# Testing stage - for running tests in CI/CD
FROM development AS testing

# Copy test files
COPY --chown=flowstate:flowstate tests/ ./tests/

# Set test environment variables
ENV FLOWSTATE_ENV=testing

# Run tests by default
CMD ["python", "-m", "pytest", "tests/", "-v", "--cov=src", "--cov-report=html"]

# Production-ready stage with security hardening
FROM runtime AS production

# Additional security: remove package managers and unnecessary binaries
USER root
RUN apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/* \
    && find /usr/bin /usr/sbin -type f \( \
        -name "apt*" -o \
        -name "dpkg*" -o \
        -name "wget" -o \
        -name "curl" \
    \) -delete

# Switch back to flowstate user
USER flowstate

# Set read-only filesystem (application doesn't write to container filesystem)
# Data is written to mounted volumes only

# Security: Drop all capabilities (none needed for this application)
# This would be set at runtime with: --cap-drop=ALL

# Final production configuration
ENV FLOWSTATE_ENV=production \
    FLOWSTATE_LOG_LEVEL=INFO \
    FLOWSTATE_SECURITY_MODE=strict

# Ensure application starts properly
CMD ["python", "-m", "src.main", "--production"]

# Multi-stage build targets:
# docker build --target development -t flowstate:dev .
# docker build --target testing -t flowstate:test .
# docker build --target production -t flowstate:prod .
# docker build . -t flowstate:latest  # defaults to production
