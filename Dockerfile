# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY app.py .

# Expose the port Cloud Run expects
EXPOSE 8080

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Run the app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
