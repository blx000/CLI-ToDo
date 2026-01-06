from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from .errors import InvalidTaskTitle


class TaskStatus(str, Enum):
    TODO = "TODO"
    DONE = "DONE"


@dataclass(frozen=True, slots=True)
class Task:
    id: int
    title: str
    status: TaskStatus
    created_at: str  # ISO string for JSON storage

    @staticmethod
    def create(task_id: int, title: str) -> "Task":
        clean_title = title.strip()
        if not clean_title:
            raise InvalidTaskTitle("Task title must not be empty.")

        now_iso = datetime.now(timezone.utc).isoformat()
        return Task(
            id=task_id,
            title=clean_title,
            status=TaskStatus.TODO,
            created_at=now_iso,
        )

    def mark_done(self) -> "Task":
        return Task(
            id=self.id,
            title=self.title,
            status=TaskStatus.DONE,
            created_at=self.created_at,
        )
