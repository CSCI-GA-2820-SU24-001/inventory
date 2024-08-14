# Inventory Service Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

[![Build Status](https://github.com/CSCI-GA-2820-SU24-001/inventory/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SU24-001/inventory/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SU24-001/inventory/graph/badge.svg?token=VR1EUO1UBG)](https://codecov.io/gh/CSCI-GA-2820-SU24-001/inventory)

## Overview

The Inventory Service is designed to manage the collection of inventory items for a business. This service allows users to perform CRUD (Create, Read, Update, Delete) operations on inventory items through a RESTful API. Each inventory item includes various attributes such as name, description, quantity, price, product_id, restock_level, and condition.

This project is structured to follow best practices in software development, including unit testing and adherence to PEP8 coding standards. It utilizes Flask as the web framework, SQLAlchemy for ORM (Object Relational Mapping), and PostgreSQL as the database.

The service is built to support seamless integration and deployment in a containerized environment using Docker, with a focus on maintainability, scalability, and ease of use.

Key features of this project include:

- **RESTful API Endpoints:** Allows clients to interact with the inventory system.
- **Database Integration:** Uses SQLAlchemy to manage interactions with the PostgreSQL database.
- **Comprehensive Testing:** Includes unit tests for models and routes to ensure reliability.
- **Logging and Error Handling:** Implements robust logging and error handling mechanisms.
- **Configuration Management:** Utilizes environment variables to manage configuration settings.
- **Documentation:** Provides clear documentation and instructions for setup, running, and testing the service.

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.gitattributes      - File to gix Windows CRLF issues

.devcontainers/     - Folder with support for VSCode Remote Containers
.tekton/            - Tekton CI/CD pipeline files
k8s/                - Kubernetes deployment files
Dockerfile          - Docker configuration file

dot-env-example     - copy to .env to use environment variables
.flaskenv           - Environment variables to configure Flask
pyproject.toml      - Poetry list of Python libraries required
wsgi.py             - WSGI entry point for the application

thunder/            - Thunder Client collection for testing APIs

service/                        - service python package
├── __init__.py                 - package initializer
├── config.py                   - configuration parameters
├── routes.py                   - module with service routes
├── common                      - common code package
│   ├── cli_commands.py         - Flask command to recreate all 
│   ├── error_handlers.py       - HTTP error handling code
│   ├── log_handlers.py         - logging setup code
│   └── status.py               - HTTP status constants
│── models.py                   - models package
│               
└── static                      - static files package
    ├── css                     - CSS files
    ├── images                  - Image files
    ├── js                      - JavaScript files
        ├── bootstrap.min.js    - Bootstrap library for 
        ├── jquery-3.6.0.min.js - jQuery library for simplified 
        └── rest_api.js         - JavaScript file for interacting 
    └── index.html              - Main HTML file for the web 

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## API Endpoints

The inventory service provides the following API endpoints:

| Operation                    | Method | URL                           |
|------------------------------|--------|-------------------------------|
| **Health check**             | GET    | `/health`                     |
| **Root URL**                 | GET    | `/`                           |
| **List all inventory items** | GET    | `/inventory`                  |
| **Create an inventory item** | POST   | `/inventory`                  |
| **Read an inventory item**   | GET    | `/inventory/{id}`             |
| **Update an inventory item** | PUT    | `/inventory/{id}`             |
| **Delete an inventory item** | DELETE | `/inventory/{id}`             |

## Running the Tests

To run the tests for this project, you can use the following command:

```bash
make test
```

## Running the Service

To run the inventory service locally, you can use the following command:

```bash
honcho start
```

The service will start and be accessible at http://localhost:8000. To change the port, update the environment variable in the .flaskenv file.

## Kubernetes Cluster

This section provides instructions on how to manage your Kubernetes cluster and deploy your application using the provided Makefile.

### Commands

- **Create a Kubernetes Cluster:**
  To create a Kubernetes cluster with a load balancer and a registry, run:
  ```sh
  make cluster
  ```
  This command creates a K3D Kubernetes cluster with one agent node and a local registry.

- **List Existing Kubernetes Clusters:**
  To list all existing K3D clusters, run:
  ```sh
  make kc-list
  ```
  This command lists all the K3D clusters currently available on your system.

- **Remove a Kubernetes Cluster:**
  To remove a Kubernetes cluster, run:
  ```sh
  make cluster-rm
  ```
  This command deletes the K3D Kubernetes cluster specified by the `CLUSTER` variable (default is `nyu-devops`).

- **Build the Docker Image:**
  To build the Docker image for your application, run:
  ```sh
  make build
  ```
  This command builds a Docker image with the tag `inventory:latest`.

- **Tag the Docker Image:**
  To create a tag for the Docker image, run:
  ```sh
  make tag
  ```
  This command tags the `inventory:latest` Docker image with `cluster-registry:5000/inventory:latest`.

- **Push the Docker Image:**
  To push the Docker image to the cluster registry, run:
  ```sh
  make push
  ```
  This command pushes the Docker image tagged as `cluster-registry:5000/inventory:latest` to the cluster registry.

if we get this error 

vscode@nyu:/app$ make push
Pushing the Docker image...
The push refers to repository [cluster-registry:5000/inventory]
Get "https://cluster-registry:5000/v2/": dial tcp: lookup cluster-registry on 127.0.0.11:53: no such host
make: *** [Makefile:76: push] Error 1

use the below command on the terminal to fix issue :
sudo bash -c "echo '127.0.0.1    cluster-registry' >> /etc/hosts"

- **Deploy the Service to Kubernetes:**
  To deploy your service to the local Kubernetes cluster, run:
  ```sh
  make deploy
  ```
  This command applies the Kubernetes configurations found in the `k8s/` directory to deploy the service.

- **Get All Kubernetes Resources:**
  To retrieve all Kubernetes resources in the current context, run:
  ```sh
  make kc-get
  ```
  This command lists all Kubernetes resources in the cluster.

### Example Workflow

1. **Create the Kubernetes Cluster:**
   ```sh
   make cluster
   ```

2. **Build and Tag the Docker Image:**
   ```sh
   make build
   make tag
   ```

3. **Push the Docker Image to the Registry:**
   ```sh
   make push
   ```

4. **Deploy the Application to Kubernetes:**
   ```sh
   make deploy
   ```

5. **List All Kubernetes Resources:**
   ```sh
   make kc-get
   ```

6. **Remove the Kubernetes Cluster:**
   ```sh
   make cluster-rm
   ```

These steps will help you manage your Kubernetes cluster and deploy your application seamlessly.

## Open Shift Deployment

The inventory service is also deployed using an OpenShift pipeline. The deployed application can be accessed at the following URL:

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.