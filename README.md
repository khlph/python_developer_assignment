# Car Listing API

This FastAPI-based API enables the management of car listings on an e-commerce platform, adhering to the given assignment instructions.

## Functionality

* Create, read, update, and delete (CRUD) operations for Cars and Brokers.
* Retrieve car listing statuses (INACTIVE, ACTIVE, SOLD).
* Implement data models using Pydantic.
* API documentation using Swagger.
* Dockerized application for easy setup and deployment.

## Technology Stack

* Python 3.11
* FastAPI, Pydantic, MongoDB

## Prerequisites

* Docker and Docker Compose

Run the following command to build and start the containers

```bash
git clone https://github.com/khlph/python_developer_assignment.git
cd python_developer_assignment

docker-compose up --build
```

## Access the API

The API will be available at http://localhost:8000/.
Explore API endpoints and interactive documentation using Swagger at http://localhost:8000/docs.

## Special Thanks

[MongoDB Developer Hub](https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/) for their Python FastAPI Quick Start guide. \
ChatGPT and Gemini Advance for assistance and guidance throughout the development process. \
Their assistance was essential in utilizing my data engineering background to create this API.
