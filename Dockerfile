# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn uvicorn

# Expose FastAPI port
EXPOSE 8000

# Run the app with Gunicorn and Uvicorn workers
# -k uvicorn.workers.UvicornWorker → makes Gunicorn run FastAPI (ASGI)
# -w 2 → number of worker processes (you can increase later)
# -b 0.0.0.0:8000 → binds to all network interfaces
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app:app", "-w", "2", "-b", "0.0.0.0:8000"]
