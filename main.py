from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import database

app = FastAPI()

database.init_db()


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
    rows = database.get_all_tasks()

    return [{"id": row[0], "title": row[1], "done": bool(row[2])} for row in rows]


@app.get("/tasks/{id}", description="Get one task")
def get_task(id: int):

    row = database.get_task(id)

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"id": row[0], "title": row[1], "done": bool(row[2])}


@app.post("/tasks", status_code=201, description="Create a task")
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    new_id = database.create_task(task.title)

    return {"id": new_id, "title": task.title, "done": False}


@app.put("/tasks/{id}", description="Update a task")
def update_task(id: int, task_update: TaskUpdate):

    if task_update.title is None and task_update.done is None:
        raise HTTPException(
            status_code=400,
            detail="Update must contain title or done",
        )

    if task_update.title is not None and not task_update.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    existing = database.get_task(id)

    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")

    title = task_update.title if task_update.title is not None else existing[1]

    done = task_update.done if task_update.done is not None else bool(existing[2])

    database.update_task(id, title, done)

    return {"id": id, "title": title, "done": done}


@app.delete("/tasks/{id}", status_code=204, description="Delete a task")
def delete_task(id: int):

    deleted = database.delete_task(id)

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return