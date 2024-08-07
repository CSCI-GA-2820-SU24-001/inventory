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
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

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
flask run
```

The service will start and be accessible at http://localhost:8000. To change the port, update the environment variable in the .flaskenv file.

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
