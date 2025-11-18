from fastapi import Depends
from src.rest_api.app.core.dependencies.base import RepositoryDependency
from src.rest_api.app.repositories.file import FileRepository
from src.rest_api.app.api.v1.files.service import FileService


# === FILE DEPENDENCIES ===


get_file_repository = RepositoryDependency(FileRepository)

def get_file_service(file_repo=Depends(get_file_repository)):
    return FileService(file_repo)
