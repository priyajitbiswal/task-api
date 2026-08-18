import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def init_db():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL
            )
            """
        )

        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                [
                    ("Learn FastAPI", False),
                    ("Build a CRUD API", False),
                    ("Test the API", True),
                ],
            )


def get_all_tasks():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT id, title, done FROM tasks")
        return cursor.fetchall()


def get_task(task_id):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, title, done FROM tasks WHERE id = %s",
            (task_id,),
        )
        return cursor.fetchone()


def create_task(title):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            RETURNING id
            """,
            (title, False),
        )
    return cursor.fetchone()[0]


def update_task(task_id, title, done):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
                UPDATE tasks
                SET title = %s, done = %s
                WHERE id = %s
                """,
            (title, done, task_id),
        )
        return cursor.rowcount


def delete_task(task_id):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,),
        )
        return cursor.rowcount
