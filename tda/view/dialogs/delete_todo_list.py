# pylint: disable = no-name-in-module
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QPushButton, QVBoxLayout

from tda.control.json_handler import delete_todo_list, get_todo_lists


class DeleteTodoList(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        self.title = QLabel("Select todo list to delete")
        self.title.setAlignment(Qt.AlignCenter)
        label_font = self.title.font()
        label_font.setPointSizeF(12)
        label_font.setBold(True)
        self.title.setFont(label_font)

        layout.addWidget(self.title)

        self.chooser_todo_list = QComboBox()
        self.chooser_todo_list.addItems(
            [todo_list.name for todo_list in get_todo_lists()]
        )
        layout.addWidget(self.chooser_todo_list)

        self.button_delete = QPushButton("Delete")
        self.button_delete.pressed.connect(self.delete)
        layout.addWidget(self.button_delete)

        self.setLayout(layout)

    def delete(self) -> None:
        delete_todo_list(self.chooser_todo_list.currentText())
        self.accept()
