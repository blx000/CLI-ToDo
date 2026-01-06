from __future__ import annotations

from .errors import TaskNotFound
from .ports import TaskRepository
from ..domain.entities import Task, TaskStatus



def add_task(repo: TaskRepository, title: str) -> Task:
    task_id = repo.next_id()
    task = Task.create(task_id, title)
    repo.add(task)
    return task


def list_tasks(repo: TaskRepository, status: TaskStatus | None = None) -> list[Task]:
    tasks = repo.list_all()
    if status is None:
        return tasks
    return [t for t in tasks if t.status == status]


def complete_task(repo: TaskRepository, task_id: int) -> Task:
    task = repo.get(task_id)
    if task is None:
        raise TaskNotFound(f"Task with id={task_id} not found.")
    done = task.mark_done()
    repo.update(done)
    return done


def delete_task(repo: TaskRepository, task_id: int) -> None:
    task = repo.get(task_id)
    if task is None:
        raise TaskNotFound(f"Task with id={task_id} not found.")
    repo.delete(task_id)
