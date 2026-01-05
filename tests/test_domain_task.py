import pytest

from todo.domain.entities import Task, TaskStatus
from todo.domain.errors import InvalidTaskTitle


def test_create_task_rejects_blank_title():
    with pytest.raises(InvalidTaskTitle):
        Task.create(1, "   ")


def test_create_task_success():
    task = Task.create(1, "Buy milk")
    assert task.id == 1
    assert task.title == "Buy milk"
    assert task.status == TaskStatus.TODO
    assert isinstance(task.created_at, str)


def test_mark_done():
    task = Task.create(1, "Buy milk")
    done_task = task.mark_done()

    assert done_task.status == TaskStatus.DONE
    assert done_task.id == task.id
    assert done_task.title == task.title
