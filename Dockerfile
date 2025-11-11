# Use lightweight Python base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (FastAPI default is 8000)
EXPOSE 8000
EXPOSE 5000
# Start both MLflow UI and FastAPI together
CMD mlflow ui --backend-store-uri file:///app/mlruns --host 0.0.0.0 --port 5000 & uvicorn app:app --host 0.0.0.0 --port 8000


# Run FastAPI app with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


