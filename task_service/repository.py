from database import new_session, TaskTable
from schemas import STaskAdd, STaskGet
from sqlalchemy import select


class TasksRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd):
        async with new_session() as session:
            task_dict = data.model_dump()
            task = TaskTable(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[STaskGet]:
        async with new_session() as session:
            quary = select(TaskTable)
            result = await session.execute(quary)
            task_models = result.scalars().all()
            tasks_schemas = [
                STaskGet.model_validate(task_orm) for task_orm in task_models
            ]
            return tasks_schemas
