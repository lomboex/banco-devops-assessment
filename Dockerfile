# Build Stage
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml .
COPY src/ src/

# Create a virtual environment and install dependencies
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install build deps and project deps
# We install with -e . to respect pyproject.toml
RUN pip install --no-cache-dir .

# Final Stage
# Use distroless for security (no shell, minimal attack surface)
FROM gcr.io/distroless/python3-debian12

WORKDIR /app

# Copy venv from builder
COPY --from=builder /app/venv /app/venv
COPY --from=builder /app/src /app/src

# Set path to use venv
ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# Run as non-root user (distroless uses nonroot:nonroot by default, uid 65532)
USER nonroot

# Expose port
EXPOSE 8000

# Command to run the application
ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
