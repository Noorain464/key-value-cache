# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY main.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 7171
EXPOSE 7171

# Start the FastAPI server with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7171", "--workers", "2"]