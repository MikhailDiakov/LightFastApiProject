# Project Setup with Docker

This project demonstrates the integration of two services (Task Service and Reminder Service) using gRPC, and their interaction through a client that retrieves tasks and displays them in a rich console output.

## Requirements

- Docker
- Docker Compose

## Setup Instructions

### 1. Clone the repository

Clone the repository to your local machine:

git clone <repository-url>
cd <repository-directory>

### 2. Build and start services

Use Docker Compose to build and start the services:

docker-compose up --build

This will build and start the following services:

- task_service: The gRPC service responsible for handling tasks.
- reminder_service: The client that interacts with the task_service and periodically retrieves tasks.
- nginx: A reverse proxy for redirecting HTTP requests.

### 3. Access the documentation

Once the services are up and running, you can access the Task Service API documentation at:

http://localhost/docs

This page will show you the available endpoints and provide an interactive interface for testing the API.
