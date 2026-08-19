# Task API

A simple CRUD API built with Python and FastAPI for managing a to-do list.

This project was built as part of the FlyRank Backend Development Track.

The project was developed progressively:

- **Assignment 1:** In-memory CRUD API
- **Assignment 2:** SQLite-backed CRUD API
- **Assignment 3:** PostgreSQL-backed CRUD API using Docker and Docker Compose

The final version runs the complete application stack with a single command using Docker Compose.

## Features

- Create tasks
- Read all tasks
- Read a single task
- Update tasks
- Delete tasks
- Input validation
- HTTP status codes
- Interactive Swagger UI documentation
- PostgreSQL database persistence
- Dockerized API and database services
- Environment-based database configuration

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- PostgreSQL
- Psycopg
- Docker
- Docker Compose

# Assignment 1 — In-Memory CRUD API

The first version of the API stored tasks in a Python list in memory.

## Swagger UI

FastAPI automatically provides interactive API documentation.

Open:

http://localhost:8000/docs

### Swagger Overview

![Swagger UI Overview](screenshots/swagger-overview.png)

### GET /tasks Example

![GET Tasks Response](screenshots/swagger-get-tasks.png)

## API Endpoints

| Method | Endpoint      | Description                          |
| ------ | ------------- | ------------------------------------ |
| GET    | `/`           | Returns information about the API    |
| GET    | `/health`     | Checks whether the server is running |
| GET    | `/tasks`      | Returns all tasks                    |
| GET    | `/tasks/{id}` | Returns a single task                |
| POST   | `/tasks`      | Creates a new task                   |
| PUT    | `/tasks/{id}` | Updates an existing task             |
| DELETE | `/tasks/{id}` | Deletes a task                       |

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

| Status Code | Meaning                   |
| ----------- | ------------------------- |
| 200         | Request successful        |
| 201         | Task created              |
| 204         | Task deleted successfully |
| 400         | Invalid request           |
| 404         | Task not found            |

# Assignment 2 — SQLite Database

Assignment 2 replaces the in-memory Python list with SQLite while keeping the same CRUD API.

## Why SQLite?

SQLite was chosen because it:

- Stores the database in a single file
- Requires no separate database server
- Requires zero additional database setup
- Survives application restarts

The API and database both work with the same `tasks.db` file, so changes made to the database are immediately reflected by the API.

## Database

The database file is:

```text
tasks.db
```

It is stored in the project root and is created automatically when the application starts.

The file is included in `.gitignore`, so it is not committed to Git. Each fresh clone creates its own `tasks.db` with the table and three seeded example tasks.

## SQLite Database Screenshot

![SQLite Database](screenshots/sqlite3-db-query.png)

## Data Persistence

Unlike the first assignment, tasks are stored in SQLite rather than only in application memory. Created, updated, and deleted tasks persist when the FastAPI server is stopped and restarted.

# Assignment 3 — PostgreSQL with Docker

Assignment 3 replaces SQLite with PostgreSQL running as a Docker container.

The database layer was moved into a separate module and the application connects to PostgreSQL using an environment variable instead of a hardcoded password.

## Environment Variables

Create a `.env` file using `.env.example`.

Required variable:

```env
DATABASE_URL=postgres://postgres:YOUR_PASSWORD@localhost:5432/tasks
```

## Run the Application

Clone the repository:

```bash
git clone https://github.com/priyajitbiswal/task-api.git
cd task-api
```

Create the environment file:

```bash
cp .env.example .env
```

Start the complete stack:

```bash
docker compose up
```

This starts:

- FastAPI application
- PostgreSQL database

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Docker Compose

The stack contains two services:

```text
docker compose
      |
      ├── api
      |     └── FastAPI application
      |
      └── db
            └── PostgreSQL database
```

The PostgreSQL service uses a Docker volume to persist data between container restarts.

Stopping and restarting the stack does not remove existing tasks.

## Database Access

Open PostgreSQL inside the database container:

```bash
docker compose exec db psql -U postgres -d tasks
```

Check tables:

```sql
\dt
```

View stored tasks:

```sql
SELECT * FROM tasks;
```

## PostgreSQL Database Screenshot

![PostgreSQL Database](screenshots/postgres-query.png)

## API Endpoints

| Method | Endpoint      | Description                          |
| ------ | ------------- | ------------------------------------ |
| GET    | `/`           | Returns information about the API    |
| GET    | `/health`     | Checks whether the server is running |
| GET    | `/tasks`      | Returns all tasks                    |
| GET    | `/tasks/{id}` | Returns a single task                |
| POST   | `/tasks`      | Creates a new task                   |
| PUT    | `/tasks/{id}` | Updates an existing task             |
| DELETE | `/tasks/{id}` | Deletes a task                       |

## Example API Request

Create a task:

```bash
curl -i -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Learn Docker Compose"}'
```

## Project Structure

```text
task-api/
├── main.py
├── database.py
├── Dockerfile
├── compose.yaml
├── .env.example
├── README.md
├── screenshots/
│   ├── swagger-overview.png
│   ├── swagger-get-tasks.png
│   ├── sqlite3-db-query.png
│   └── postgres-query.png
├── pyproject.toml
├── uv.lock
└── .gitignore
```

## Author

Priyajit Biswal
