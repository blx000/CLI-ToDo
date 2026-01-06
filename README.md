
# CLI ToDo

CLI ToDo - консольное CRUD-приложение для управления списком задач
с хранением данных в JSON-файле.

Проект выполнен в учебных целях с использованием:
- слоистой архитектуры (Domain / Application / Infrastructure / Presentation)
- git-flow
- CI (GitHub Actions)

---

## Функциональность

- Добавление задач
- Просмотр списка задач
- Фильтрация задач по статусу
- Отметка задач как выполненных
- Удаление задач

---

## Архитектура проекта

Проект разделён на слои:

- **Domain** (`src/todo/domain`) - доменная модель и бизнес-правила  
- **Application** (`src/todo/application`) - use-cases и порт репозитория  
- **Infrastructure** (`src/todo/infrastructure`) - JSON-хранилище  
- **Presentation** (`src/todo/presentation`) - CLI-интерфейс  

---

## Требования

- Python 3.13+

---

## Установка

```bash
git clone https://github.com/blx000/CLI-ToDo.git
cd CLI-ToDo

python -m venv .venv
source .venv/bin/activate
````

---

## Использование

Приложение запускается как Python-модуль:

```bash
python -m todo <command> [arguments]
```

---

## Доступные команды CLI

### Добавить задачу

```bash
python -m todo add "Buy milk"
```

---

### Показать все задачи

```bash
python -m todo list
```

---

### Показать задачи по статусу

Невыполненные:

```bash
python -m todo list --status todo
```

Выполненные:

```bash
python -m todo list --status done
```

---

### Отметить задачу выполненной

```bash
python -m todo done <task_id>
```

Пример:

```bash
python -m todo done 1
```

---

### Удалить задачу

```bash
python -m todo delete <task_id>
```

Пример:

```bash
python -m todo delete 1
```

---

## Хранилище данных

Файл:

```
data/tasks.json
```

Пример:

```json
{
  "next_id": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Buy milk",
      "status": "DONE",
      "created_at": "2026-01-07T12:00:00+00:00"
    }
  ]
}
```

---

## Тестирование

```bash
pytest -q
```

---

## CI

При каждом push и pull request в ветку `develop`
автоматически запускаются:

* линтер (`ruff`)
* тесты (`pytest`)

