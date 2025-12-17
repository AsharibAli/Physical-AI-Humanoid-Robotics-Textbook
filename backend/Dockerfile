# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy dependency files to backend subdirectory
COPY pyproject.toml uv.lock ./backend/

# Install dependencies
WORKDIR /app/backend
RUN uv sync --frozen --no-dev

# Copy application code to backend subdirectory
WORKDIR /app
COPY . ./backend/

# Set PYTHONPATH so Python can find the backend module
ENV PYTHONPATH=/app

# Expose port (Railway will inject $PORT)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/api/v1/health', timeout=5)"

# Run the application
WORKDIR /app/backend
CMD ["uv", "run", "uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]