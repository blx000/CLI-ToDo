# CLI ToDo

Консольное ToDo-приложение с JSON-хранилищем.

## Возможности
- Добавление задачи
- Просмотр списка задач
- Завершение задачи
- Удаление задачи
- Фильтрация по статусу

## Архитектура
Проект разделён на слои:
- **Domain** - сущности и бизнес-правила
- **Application** - use-cases и порты (интерфейсы)
- **Infrastructure** - реализация репозитория (JSON)
- **Presentation** - CLI интерфейс

Структура проекта использует `src`-layout, поэтому запуск идёт через `python -m src.todo`.

## Установка
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install pytest ruff
