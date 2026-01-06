from __future__ import annotations

import argparse
from pathlib import Path

from ..application.errors import TaskNotFound
from ..application.use_cases import add_task, complete_task, delete_task, list_tasks
from ..domain.entities import TaskStatus
from ..infrastructure.json_repo import JsonTaskRepository



def _repo() -> JsonTaskRepository:
    return JsonTaskRepository(Path("data") / "tasks.json")


def cmd_add(args: argparse.Namespace) -> int:
    task = add_task(_repo(), args.title)
    print(f"Added: [{task.id}] {task.title} ({task.status})")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    status = None
    if args.status == "todo":
        status = TaskStatus.TODO
    elif args.status == "done":
        status = TaskStatus.DONE

    tasks = list_tasks(_repo(), status=status)
    if not tasks:
        print("No tasks.")
        return 0

    for t in tasks:
        mark = "✓" if t.status == TaskStatus.DONE else " "
        print(f"[{t.id:03}] [{mark}] {t.title}")
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    try:
        task = complete_task(_repo(), args.id)
    except TaskNotFound as e:
        print(str(e))
        return 1
    print(f"Done: [{task.id}] {task.title}")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    try:
        delete_task(_repo(), args.id)
    except TaskNotFound as e:
        print(str(e))
        return 1
    print(f"Deleted task id={args.id}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="CLI ToDo (JSON storage)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", type=str, help='Task title in quotes, e.g. "Buy milk"')
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--status", choices=["all", "todo", "done"], default="all")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="Mark task as done")
    p_done.add_argument("id", type=int)
    p_done.set_defaults(func=cmd_done)

    p_del = sub.add_parser("delete", help="Delete task")
    p_del.add_argument("id", type=int)
    p_del.set_defaults(func=cmd_delete)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
