# Use the official Python slim image as a base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first (to leverage Docker layer caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app /app/app

# Expose port 8000 for Uvicorn
EXPOSE 8000

# Default command to run Uvicorn with your FastAPI app
# Adjust "app.main:app" if your main.py is in a different location
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
