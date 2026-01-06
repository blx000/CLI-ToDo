import pytest

from todo.application.errors import TaskNotFound
from todo.application.use_cases import add_task, complete_task, delete_task, list_tasks
from todo.domain.entities import Task, TaskStatus


class FakeRepo:
    def __init__(self):
        self._next_id = 1
        self._tasks: dict[int, Task] = {}

    def next_id(self) -> int:
        nid = self._next_id
        self._next_id += 1
        return nid

    def list_all(self) -> list[Task]:
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def add(self, task: Task) -> None:
        self._tasks[task.id] = task

    def get(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def update(self, task: Task) -> None:
        self._tasks[task.id] = task

    def delete(self, task_id: int) -> None:
        self._tasks.pop(task_id, None)


def test_add_and_list():
    repo = FakeRepo()
    add_task(repo, "A")
    add_task(repo, "B")
    tasks = list_tasks(repo)
    assert [t.title for t in tasks] == ["A", "B"]


def test_complete_task():
    repo = FakeRepo()
    t = add_task(repo, "Do homework")
    done = complete_task(repo, t.id)
    assert done.status == TaskStatus.DONE


def test_complete_missing_task():
    repo = FakeRepo()
    with pytest.raises(TaskNotFound):
        complete_task(repo, 999)


def test_delete_task():
    repo = FakeRepo()
    t = add_task(repo, "X")
    delete_task(repo, t.id)
    assert list_tasks(repo) == []


def test_delete_missing_task():
    repo = FakeRepo()
    with pytest.raises(TaskNotFound):
        delete_task(repo, 999)
