# wier-24


[![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)](https://www.docker.com/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)](https://jupyter.org/)
[![Spider](https://img.shields.io/badge/Pajki-🕷-red?)](https://www.youtube.com/watch?v=_apkTbq6grk)

# About the project
The project is a web crawler that utilizes Selenium and other libraries to scrape data from websites. It communicates with a PostgreSQL database hosted on the cloud through a Flask API. The entire project is containerized using Docker for easy deployment and scalability.

# Running the web crawler

The web crawler is part of a larger project architecture that is split into three Docker containers. These containers are managed by a centralized Docker Compose file.

## Client Container
The client container contains the Jupyter Notebook environment, which is used for running the web crawler. The Dockerfile for the client container is located in the client directory. It sets up the Jupyter Notebook environment within a Conda virtual environment, providing a clean and isolated environment for running the code.

## API Container
The API container hosts a Flask API that acts as the communication layer between the client and the cloud SQL database. It handles requests from the client and interacts with the database via the Cloud SQL Proxy. The API directory contains the necessary code and configuration files for running the Flask API.

## Cloud SQL Database
The project utilizes a PostgreSQL database hosted on the cloud. The API container communicates with the database through the Cloud SQL Proxy, which provides a secure and reliable connection.

To run the web crawler and the entire project, follow these steps:

1. Create and configure the `.env` file in the root directory. This file should contain the necessary environment variables for the project, such as database credentials and service account file name.

2. Insert a valid `service-account.json` file in the root directory. This file is required for authenticating with the cloud SQL database.

3. Build the Docker image:
    ```
    > docker compose build
    ```

4. Run the Docker containers:
    ```
    > docker compose up
    ```

5. Access the Jupyter Notebook environment:
    Open your web browser and navigate to `localhost:8888`.

6. Access the API:
    The API for database operations is available at `localhost:5000`.

This will start the project and allow you to run the web crawler within the Jupyter Notebook environment.