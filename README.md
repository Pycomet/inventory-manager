# Inventory Management System

## Overview

This project is a simple Inventory Management System for an e-commerce platform. It supports basic CRUD operations for managing items in inventory and is designed to handle a high volume of concurrent read and write operations.

## Technologies Used

- FastAPI: Used for building the API endpoints.
- Prisma: Used for database operations, providing a modern and type-safe approach.
- SQLite: Chosen for simplicity. In a production environment, a more robust database like PostgreSQL could be used.
- Docker: Used for containerization to allow horizontal scalability.

## API Endpoints

- `POST /items/`: Add a new item to the inventory.
- `GET /items/{sku}`: Retrieve information about an item based on its SKU.
- `PUT /items/{sku}`: Modify existing items (e.g., quantity, price, etc.).
- `DELETE /items/{sku}`: Remove items from inventory.

## Running the Project

1. Install Docker and Docker Compose.
2. Clone the repository.
3. Build and run the Docker containers: `docker-compose up`.

Access the API at http://localhost:8000.

## Architectural Decisions

- Dockerization: The application is containerized along with the Prisma database to allow for easy scaling horizontally by spinning up multiple containers.
- Prisma: Chosen for its modern and type-safe approach to database operations, improving code reliability and maintainability.
- SQLite: Chosen for simplicity. In a production environment, a more robust database like PostgreSQL could be used.
- FastAPI: Chosen for its high performance and asynchronous capabilities, making it suitable for handling concurrent operations.

