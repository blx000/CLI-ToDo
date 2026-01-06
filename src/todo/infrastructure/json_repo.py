from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from todo.domain.entities import Task, TaskStatus


class JsonTaskRepository:
    """
    JSON format:
    {
      "next_id": 1,
      "tasks": [
        {"id":1,"title":"...","status":"TODO","created_at":"..."}
      ]
    }
    """

    def __init__(self, file_path: str | Path):
        self._path = Path(file_path)
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._write({"next_id": 1, "tasks": []})

    def _read(self) -> dict:
        with self._path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: dict) -> None:
        tmp = self._path.with_suffix(self._path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(self._path)

    def _task_from_dict(self, raw: dict) -> Task:
        return Task(
            id=int(raw["id"]),
            title=str(raw["title"]),
            status=TaskStatus(str(raw["status"])),
            created_at=str(raw["created_at"]),
        )

    def _task_to_dict(self, task: Task) -> dict:
        d = asdict(task)
        d["status"] = task.status.value
        return d

    def next_id(self) -> int:
        data = self._read()
        nid = int(data["next_id"])
        data["next_id"] = nid + 1
        self._write(data)
        return nid

    def list_all(self) -> list[Task]:
        data = self._read()
        tasks = [self._task_from_dict(t) for t in data.get("tasks", [])]
        return sorted(tasks, key=lambda t: t.id)

    def add(self, task: Task) -> None:
        data = self._read()
        data.setdefault("tasks", []).append(self._task_to_dict(task))
        self._write(data)

    def get(self, task_id: int) -> Task | None:
        data = self._read()
        for raw in data.get("tasks", []):
            if int(raw["id"]) == int(task_id):
                return self._task_from_dict(raw)
        return None

    def update(self, task: Task) -> None:
        data = self._read()
        tasks = data.get("tasks", [])
        for i, raw in enumerate(tasks):
            if int(raw["id"]) == int(task.id):
                tasks[i] = self._task_to_dict(task)
                data["tasks"] = tasks
                self._write(data)
                return

    def delete(self, task_id: int) -> None:
        data = self._read()
        tasks = data.get("tasks", [])
        data["tasks"] = [t for t in tasks if int(t["id"]) != int(task_id)]
        self._write(data)
