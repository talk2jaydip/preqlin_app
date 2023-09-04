# Use the official Python image as the base image
FROM python:3.7-slim

# Set environment variables to prevent Python from writing pyc files and for unbuffered output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Create a directory for data if needed
RUN mkdir /data

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY my_app /app/my_app

# Copy the remaining application files into the container
COPY . /app/

# Read the FLASK_PORT value from the environment file
ENV FLASK_PORT=$FLASK_PORT

# Expose the port specified in the FLASK_PORT environment variable
EXPOSE "$FLASK_PORT"

# Define the entry point to run the application
#CMD ["python", "run.py"]
