# pylint: disable = no-name-in-module
from __future__ import annotations

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from tda.control.json_handler import save_todos
from tda.model.todo_list import TodoList
from tda.view.widgets.todo_widget import TodoWidget


class TodoListWidget(QWidget):
    objects: list[TodoListWidget] = []

    refresh = pyqtSignal()

    def __init__(self, parent, todo_list: TodoList) -> None:
        super().__init__(parent)

        self.todo_list = todo_list
        self.todo_widgets: list[TodoWidget] = []

        self.setup_ui()
        TodoListWidget.objects.append(self)

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.label_name = QLabel(self.todo_list.name)
        self.label_name.setAlignment(Qt.AlignCenter)
        label_font = self.label_name.font()
        label_font.setPointSizeF(20)
        label_font.setBold(True)
        self.label_name.setFont(label_font)

        layout.addWidget(self.label_name)
        for todo in self.todo_list.todos:
            todo_widget = TodoWidget(self, todo)
            todo_widget.deleted.connect(todo_widget.deleteLater)
            todo_widget.deleted.connect(save_todos)
            todo_widget.deleted.connect(self.refresh)
            layout.addWidget(todo_widget)
            self.todo_widgets.append(todo_widget)

        separator = QFrame(self)
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Plain)

        layout.addWidget(separator)

        vertical_spacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        layout.addItem(vertical_spacer)

        self.setLayout(layout)
