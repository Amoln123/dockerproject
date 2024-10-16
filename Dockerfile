# Use the official Python image with version 3.12.3
FROM python:3.10.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to where manage.py is located
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire project code into the container
COPY . .

# Expose the port the app runs on (Django default port)
EXPOSE 8000

# Start the Django server using the manage.py script with your settings module
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=user_service.settings"]
