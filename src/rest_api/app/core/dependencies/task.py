from fastapi import Depends
from src.rest_api.app.core.dependencies.base import RepositoryDependency
from src.rest_api.app.repositories.task import TaskRepository
from src.rest_api.app.api.v1.tasks.service import TaskService


# === TASK DEPENDENCIES ===


get_task_repository = RepositoryDependency(TaskRepository)

def get_task_service(task_repo=Depends(get_task_repository)):
    return TaskService(task_repo)
