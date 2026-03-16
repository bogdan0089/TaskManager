from database.database import Base
from typing import List
from sqlalchemy import ForeignKey, Table, Column, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.enum import TaskStatus, UserRole


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[List["Task"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")
    


