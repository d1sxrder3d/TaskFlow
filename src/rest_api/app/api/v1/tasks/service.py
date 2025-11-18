from src.rest_api.app.core.bases.service import BaseService
from src.rest_api.app.repositories.task import TaskRepository
from src.rest_api.app.models.task import Task



class TaskService(BaseService[Task, TaskRepository]):
    def __init__(self, task_repository: TaskRepository):
        super().__init__(task_repository)

    async def get_tasks_by_user(self, user_id: int) -> list[Task]:
        return await self.repo.get_by_user(user_id)

    async def get_tasks_by_tag(self, tag_id: int) -> list[Task]:
        return await self.repo.get_by_tag(tag_id)
