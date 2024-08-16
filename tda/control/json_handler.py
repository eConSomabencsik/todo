import json
import os
from typing import List

from tda.model.todo import Todo
from tda.model.todo_list import TodoList

TODO_LIST_PATH: str = os.path.join(os.path.expanduser("~"), "todos.json")


def read_todos() -> None:
    Todo.objects = []
    Todo._id = 0
    TodoList.objects = []
    TodoList._id = 0

    if not os.path.exists(TODO_LIST_PATH):
        with open(TODO_LIST_PATH, "w", encoding="UTF-8") as f:
            json.dump({}, f)

    with open(TODO_LIST_PATH, "r", encoding="UTF-8") as file:
        todo_json = json.load(file)

    for todo_list_name, todos in todo_json.items():
        todo_list = TodoList(todo_list_name)
        for todo in todos:
            todo_list.add_todo(todo["name"], todo["description"], todo["completed"])


def save_todos() -> None:
    todo_json = {}
    for todo_list in TodoList.objects:
        todo_json[todo_list.name] = []
        for todo in todo_list.todos:
            todo_json[todo_list.name].append(todo.to_dict())

    with open(TODO_LIST_PATH, "w", encoding="UTF-8") as file:
        json.dump(todo_json, file, indent=4)


def get_todo_lists() -> List[TodoList]:
    return TodoList.objects


def add_todo_list(name: str) -> None:
    TodoList(name)


def add_todo(todo_list_name: str, name: str) -> None:
    todo_list = None
    for t_l in TodoList.objects:
        if t_l.name != todo_list_name:
            continue
        todo_list = t_l

    if todo_list is None:
        return

    todo_list.add_todo(name)
    save_todos()


def delete_todo(todo: Todo) -> None:
    for todo_list in TodoList.objects:
        if todo not in todo_list.todos:
            continue
        todo_list.todos.remove(todo)

    Todo.objects.remove(todo)
    save_todos()


def delete_todo_list(todo_list_name: str) -> None:
    current_todo_list = None
    for todo_list in TodoList.objects:
        if todo_list.name != todo_list_name:
            continue
        current_todo_list = todo_list

    if current_todo_list is None:
        return

    TodoList.objects.remove(current_todo_list)
    save_todos()
