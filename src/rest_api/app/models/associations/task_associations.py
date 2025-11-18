from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint

from src.rest_api.app.core.bases import BaseModel

association_task_tag = Table(
    "tasks_tags",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("task_id", ForeignKey("tasks.id"), nullable=False),
    Column("tag_id", ForeignKey("tags.id"), nullable=False),
    UniqueConstraint("task_id", "tag_id", name="uq_task_tag")
)
