# Use an official Python runtime as a base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port for the FastAPI application (default for Uvicorn)
EXPOSE 8000

# This CMD is a placeholder; Dagster will define actual execution commands.
# We keep the container running for easier debugging during development.
CMD ["tail", "-f", "/dev/null"]