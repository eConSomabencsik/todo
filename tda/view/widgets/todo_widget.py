# pylint: disable = no-name-in-module
from __future__ import annotations

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QCheckBox, QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from tda.control.json_handler import delete_todo, save_todos
from tda.model.todo import Todo


class TodoWidget(QWidget):
    objects: list[TodoWidget] = []

    deleted = pyqtSignal()

    def __init__(self, parent, todo: Todo) -> None:
        super().__init__(parent)

        self.todo = todo

        self.has_focus = False

        self.setup_ui()
        TodoWidget.objects.append(self)

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.label_name = QLabel(self.todo.name)
        label_font = self.label_name.font()
        label_font.setPointSizeF(16)
        self.label_name.setFont(label_font)

        self.check_completed = QCheckBox("Completed")
        self.check_completed.stateChanged.connect(self.complete_todo)
        self.check_completed.setChecked(self.todo.completed)
        self.check_completed.setFocusPolicy(Qt.NoFocus)

        self.button_delete = QPushButton()
        self.button_delete.setText("Delete")
        self.button_delete.setFocusPolicy(Qt.NoFocus)
        self.button_delete.pressed.connect(self.delete_todo)

        layout.addWidget(self.label_name)
        layout.addWidget(self.check_completed)
        layout.addWidget(self.button_delete)

        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Plain)

        layout.addWidget(separator)

        self.setLayout(layout)

    def complete_todo(self, state: int) -> None:
        completed = True if state else False
        self.todo.completed = completed
        font = self.label_name.font()
        font.setStrikeOut(completed)
        self.label_name.setFont(font)

        save_todos()

    def delete_todo(self) -> None:
        delete_todo(self.todo)
        self.deleted.emit()

    def set_focus(self, toggle: bool) -> None:
        self.has_focus = toggle
        if toggle:
            self.setStyleSheet("background-color: rgb(150, 150, 150);")
        else:
            self.setStyleSheet("")
