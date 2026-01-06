from pathlib import Path

from todo.application.use_cases import add_task, complete_task, list_tasks
from todo.domain.entities import TaskStatus
from todo.infrastructure.json_repo import JsonTaskRepository


def test_json_repo_persists_tasks(tmp_path: Path):
    file_path = tmp_path / "tasks.json"
    repo = JsonTaskRepository(file_path)

    t1 = add_task(repo, "A")
    t2 = add_task(repo, "B")

    tasks = list_tasks(repo)
    assert [t.id for t in tasks] == [t1.id, t2.id]

    complete_task(repo, t1.id)
    done = list_tasks(repo, TaskStatus.DONE)
    assert [t.id for t in done] == [t1.id]
