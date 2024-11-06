# Use the specific Python 3.10.12 image as the base
FROM python:3.10.12-slim

# Install dependencies for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# Expose the Flask app port
EXPOSE 8000

# Set environment variables
ENV FLASK_ENV=production

# Start the Flask app
CMD ["python", "app.py"]
