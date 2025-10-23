# Use official Python slim image for lightweight container
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY configs/ ./configs/
COPY models/ ./models/

# Expose API and Prometheus metrics ports
EXPOSE 8000 9090

# Command to run the application
CMD ["python", "src/main.py"]