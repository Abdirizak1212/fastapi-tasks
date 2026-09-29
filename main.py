from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import database, tasks

app = FastAPI()

class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

class TaskOut(TaskIn):
    id: int

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/tasks", response_model=List[TaskOut])
async def list_tasks():
    query = tasks.select()
    return await database.fetch_all(query)

@app.post("/tasks", response_model=TaskOut)
async def create_task(task: TaskIn):
    query = tasks.insert().values(
        title=task.title,
        description=task.description,
        status=task.status,
        date=task.date,
        time=task.time,
    )
    task_id = await database.execute(query)
    return {"id": task_id, **task.dict()}

@app.get("/tasks/{task_id}", response_model=TaskOut)
async def get_task(task_id: int):
    query = tasks.select().where(tasks.c.id == task_id)
    row = await database.fetch_one(query)
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    return row

@app.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task: TaskIn):
    query = tasks.update().where(tasks.c.id == task_id).values(
        title=task.title,
        description=task.description,
        status=task.status,
        date=task.date,
        time=task.time,
    )
    await database.execute(query)
    return {"id": task_id, **task.dict()}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {"status": "deleted"}
