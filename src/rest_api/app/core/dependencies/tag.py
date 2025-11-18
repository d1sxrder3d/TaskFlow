from fastapi import Depends
from src.rest_api.app.core.dependencies.base import RepositoryDependency
from src.rest_api.app.repositories.tag import TagRepository
from src.rest_api.app.api.v1.tags.service import TagService


# === TAG DEPENDENCIES ===


get_tag_repository = RepositoryDependency(TagRepository)


def get_tag_service(tag_repo=Depends(get_tag_repository)):
    return TagService(tag_repo)
