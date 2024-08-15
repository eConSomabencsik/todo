# pylint: disable = no-name-in-module
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

from tda.control import json_handler


class AddTodoListDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        self.title = QLabel("Add Todo List")
        self.title.setAlignment(Qt.AlignCenter)
        label_font = self.title.font()
        label_font.setPointSizeF(12)
        label_font.setBold(True)
        self.title.setFont(label_font)

        self.input_name = QLineEdit()
        self.button_add = QPushButton("Add list")
        self.button_add.pressed.connect(self.add)

        layout.addWidget(self.title)
        layout.addWidget(self.input_name)
        layout.addWidget(self.button_add)

        self.setLayout(layout)

    def add(self) -> None:
        name = self.input_name.text()
        if name.strip() == "":
            return
        json_handler.add_todo_list(name)
        self.accept()
