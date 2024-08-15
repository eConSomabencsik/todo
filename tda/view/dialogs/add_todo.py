# pylint: disable = no-name-in-module
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from tda.control import json_handler
from tda.model.todo_list import TodoList


class AddTodoDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        self.title = QLabel("Add Todo")

        self.title.setAlignment(Qt.AlignCenter)
        label_font = self.title.font()
        label_font.setPointSizeF(12)
        label_font.setBold(True)
        self.title.setFont(label_font)

        self.choose_todo_list = QComboBox()
        self.choose_todo_list.addItems(
            [todo_list.name for todo_list in TodoList.objects]
        )
        self.input_name = QLineEdit()
        self.button_add = QPushButton("Add todo")
        self.button_add.pressed.connect(self.add)

        layout.addWidget(self.title)
        layout.addWidget(self.choose_todo_list)
        layout.addWidget(self.input_name)
        layout.addWidget(self.button_add)

        self.setLayout(layout)

    def add(self) -> None:
        name = self.input_name.text()
        todo_list_name = self.choose_todo_list.currentText()
        if name.strip() == "":
            return
        json_handler.add_todo(todo_list_name, name)
        self.accept()
