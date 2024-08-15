from __future__ import annotations


class Todo:

    _id: int = 0
    objects: list[Todo] = []

    def __init__(
        self, name: str, description: str = "", completed: bool = False
    ) -> None:
        self._id = Todo._id
        self.name = name
        self.description = description
        self.completed = completed

        Todo._id += 1
        Todo.objects.append(self)

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "name": self.name,
            "description": self.description,
            "completed": self.completed,
        }
