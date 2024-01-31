from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class Task(BaseModel):
    title: str
    description: str
    status: bool


tasks_db = []
task_id_counter = 1


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    global task_id_counter
    task_data = task.model_dump()
    task_data["id"] = task_id_counter
    task_id_counter += 1
    tasks_db.append(task_data)
    return task_data


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.update(updated_task.model_dump(exclude_unset=True))
    return task


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks_db.remove(task)
    return task
