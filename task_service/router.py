from fastapi import APIRouter, HTTPException
from typing import Annotated
from fastapi import Depends
from schemas import STaskAdd, STaskGet, STaskId
from repository import TasksRepository

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("")
async def add_task(
    task: Annotated[STaskAdd, Depends()],
) -> STaskId:
    task_id = await TasksRepository.add_one(task)
    return {"ok": True, "task_id": task_id}

@router.get("")
async def get_tasks() -> list[STaskGet]:
    tasks = await TasksRepository.find_all()
    return tasks

@router.delete("/{task_id}")
async def delete_task(task_id: int):
    deleted = await TasksRepository.delete_one(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True, "message": f"Task {task_id} deleted"}
