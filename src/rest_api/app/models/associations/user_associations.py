from enum import Enum as PyEnum
from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint, Enum

from src.rest_api.app.core.bases import BaseModel



class UserRole(str, PyEnum):
    OWNER = "owner"
    MANAGER = "manager"
    EMPLOYEE = "employee"

association_user_organization = Table(
    "users_organizations",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("organization_id", ForeignKey("organizations.id"), nullable=False),
    Column("user_role", Enum(UserRole), nullable=False, default=UserRole.EMPLOYEE),
    UniqueConstraint('user_id', 'organization_id', name='uq_user_organization')
)


association_user_project = Table(
    "users_projects",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("project_id", ForeignKey("projects.id"), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("user_role", Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False),
    UniqueConstraint("project_id", "user_id", name="uq_project_user")
)


association_user_task = Table(
    "users_tasks",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("task_id", ForeignKey("tasks.id"), nullable=False),
    UniqueConstraint("user_id", "task_id", name="uq_user_task")
)