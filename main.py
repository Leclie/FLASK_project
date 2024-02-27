from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Task(BaseModel):
    title: str
    description: str
    status: bool = False

tasks = []

# GET /tasks
@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks

# GET /tasks/{id}
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task.get("id") == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# POST /tasks
@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    new_task = task.dict()
    new_task["id"] = len(tasks) + 1
    tasks.append(new_task)
    return new_task

# PUT /tasks/{id}
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    for t in tasks:
        if t.get("id") == task_id:
            t.update(task.dict())
            return t
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE /tasks/{id}
@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.get("id") == task_id:
            del tasks[i]
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/app", response_class=HTMLResponse)
async def read_tasks(request: Request):
    return templates.TemplateResponse("app.html", {"request": request, "tasks": tasks})