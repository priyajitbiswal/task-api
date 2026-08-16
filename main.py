import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

connection = sqlite3.connect("tasks.db")

connection.execute(
    """CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL)"""
)

connection.commit()

result = connection.execute("SELECT COUNT(*) FROM tasks")
count = result.fetchone()[0]

if count == 0:
    connection.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)", ("Learn FastAPI", 0)
    )

    connection.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)", ("Build a CRUD API", 0)
    )

    connection.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)", ("Test the API", 1)
    )

    connection.commit()


# tasks = [
#     {"id": 1, "title": "Learn FastAPI", "done": False},
#     {"id": 2, "title": "Build a CRUD API", "done": False},
#     {"id": 3, "title": "Test the API", "done": True},
# ]


class TaskCreate(BaseModel):
    title: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.get("/", description="Returns information about the Task API.")
def home():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", description="Check whether server is running.")
def health_check():
    return {"status": "ok"}


@app.get("/tasks", description="Get all tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{id}", description="Get one task")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@app.post("/tasks", status_code=201, description="Create a task")
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    next_id = max(t["id"] for t in tasks) + 1

    new_task = {"id": next_id, "title": task.title, "done": False}

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{id}", description="Update a task")
def update_task(id: int, task_update: TaskUpdate):

    for task in tasks:
        if task["id"] == id:
            if task_update.title is None and task_update.done is None:
                raise HTTPException(
                    status_code=400, detail="Update must contain title or done"
                )

            if task_update.title is not None:
                if not task_update.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = task_update.title

            if task_update.done is not None:
                task["done"] = task_update.done

            return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@app.delete("/tasks/{id}", status_code=204, description="Delete a task")
def delete_task(id: int):

    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return

    raise HTTPException(status_code=404, detail=f"Task {id} not found")
