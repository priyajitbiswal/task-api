# Task API

A simple CRUD API built with Python and FastAPI for managing a to-do list.

This project was built as part of the FlyRank Backend Development Track – Week 2 assignment.

## Features

- Create tasks
- Read all tasks
- Read a single task
- Update tasks
- Delete tasks
- Input validation
- HTTP status codes
- Interactive Swagger UI documentation
- In-memory task storage

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/priyajitbiswal/task-api.git
cd task-api
```

### 2. Install dependencies

This project uses the dependencies defined in `pyproject.toml`.

If you are using `uv`:

```bash
uv sync
```

### 3. Start the server

```bash
uv run uvicorn main:app --reload
```

The API will be available at:

http://localhost:8000

## Swagger UI

FastAPI automatically provides interactive API documentation.

Open:

http://localhost:8000/docs

### Swagger Overview

![Swagger UI Overview](swagger-overview.png)

### GET /tasks Example

![GET Tasks Response](swagger-get-tasks.png)

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns information about the API |
| GET | `/health` | Checks whether the server is running |
| GET | `/tasks` | Returns all tasks |
| GET | `/tasks/{id}` | Returns a single task |
| POST | `/tasks` | Creates a new task |
| PUT | `/tasks/{id}` | Updates an existing task |
| DELETE | `/tasks/{id}` | Deletes a task |

## Example

### Create a task

```bash
curl -i -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Buy milk"}'
```

Example response:

```text
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

### Get all tasks

```bash
curl -i http://localhost:8000/tasks
```

### Update a task

```bash
curl -i -X PUT http://localhost:8000/tasks/4 \
-H "Content-Type: application/json" \
-d '{"done":true}'
```

### Delete a task

```bash
curl -i -X DELETE http://localhost:8000/tasks/4
```

## Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Task created |
| 204 | Task deleted successfully |
| 400 | Invalid request |
| 404 | Task not found |

## Data Storage

Tasks are stored in an in-memory Python list.

This means that newly created or modified tasks are lost when the server restarts.

There is intentionally no database in this version of the project.

## Project Structure

```text
task-api/
├── main.py
├── README.md
├── pyproject.toml
├── uv.lock
└── .gitignore
```

## Author

Priyajit Biswal
