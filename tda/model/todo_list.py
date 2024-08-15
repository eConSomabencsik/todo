from __future__ import annotations

from tda.model.todo import Todo


class TodoList:
    _id: int = 0
    objects: list[TodoList] = []

    def __init__(self, name: str) -> None:
        self._id = TodoList._id
        self.name = name

        self.todos: list[Todo] = []

        TodoList._id += 1
        TodoList.objects.append(self)

    def add_todo(
        self, todo_message: str, description: str = "", completed: bool = False
    ):
        self.todos.append(Todo(todo_message, description, completed))
