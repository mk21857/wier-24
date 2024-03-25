# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir Flask Flask-HTTPAuth psycopg2-binary cryptography bcrypt

# Command to run the API server
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000", "--cert=adhoc"]
