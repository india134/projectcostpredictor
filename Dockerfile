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
# Expose ports for both services
EXPOSE 8000
EXPOSE 5000

# Install supervisor
RUN apt-get update && apt-get install -y supervisor

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run both MLflow and FastAPI under supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

