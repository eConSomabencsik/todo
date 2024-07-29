import json
from typing import Dict, List

TODO_LIST_PATH: str = "todos.json"


def read_todos() -> Dict[str, List[str]]:
    with open(TODO_LIST_PATH, "r", encoding="UTF-8") as file:
        todos = json.load(file)
    return todos


def save_todos(todos: Dict[str, List[str]]) -> None:
    with open(TODO_LIST_PATH, "w", encoding="UTF-8") as file:
        json.dump(todos, file, indent=4)


def delete_todo(list_name: str, todo: str) -> None:
    todos = read_todos()
    todo_to_remove: str = ""
    for t in todos[list_name]:
        t = t.replace(" (Completed)", "")
        if t in todo:
            todo_to_remove = t
            break
    todos[list_name].remove(todo_to_remove)

    save_todos(todos)


def mark_completed(list_name: str, todo: str, completed: bool) -> None:
    todos = read_todos()

    todo_to_mark: str = ""
    for todo in todos[list_name]:
        if todo in todo:
            todo_to_mark = todo
            break

    new_todo = (
        f"{todo_to_mark} (Completed)"
        if completed
        else todo_to_mark.replace(" (Completed)", "")
    )
    idx = todos[list_name].index(todo_to_mark)
    todos[list_name][idx] = new_todo

    save_todos(todos)


def add_todo(list_name: str, todo: str) -> None:
    todos = read_todos()
    todos[list_name].append(todo)
    save_todos(todos)


def add_todo_list(list_name: str) -> None:
    todos = read_todos()
    todos[list_name] = []
    save_todos(todos)


def delete_todo_list(list_name: str) -> None:
    todos = read_todos()
    del todos[list_name]
    save_todos(todos)
