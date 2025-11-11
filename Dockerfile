# Use lightweight Python base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (FastAPI default is 8000)
# Expose ports
EXPOSE 8000
EXPOSE 5000

# Start both MLflow UI and FastAPI using sh
CMD sh -c "mlflow ui --backend-store-uri file:///app/mlruns --host 0.0.0.0 --port 5000 --serve-artifacts --cors-allow-origins '*' & \
           uvicorn app:app --host 0.0.0.0 --port 8000"


