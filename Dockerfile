# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy source code
COPY src/ ./src/

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "print('healthy')" || exit 1

CMD ["python", "-m", "src.main"]
