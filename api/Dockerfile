# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the src directory into the container at /app
COPY ./src/ /app

# Install dependencies (excluding cloud-sql-proxy)
RUN pip install --no-cache-dir Flask Flask-HTTPAuth psycopg2-binary cryptography bcrypt google-auth python-dotenv

# Entrypoint for your Flask application
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000", "--cert=adhoc", "--debugger", "--reload"]
