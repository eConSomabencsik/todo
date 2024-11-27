from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
)

from tda.control.json_handler import save_todos
from tda.model.todo import Todo
from tda.model.todo_list import TodoList


class TodoDetail(QDialog):
    def __init__(self, todo: Todo, todo_list: TodoList) -> None:
        super().__init__()
        self.todo = todo
        self.todo_list = todo_list

        self.setup_ui()

    def setup_ui(self) -> None:
        self.setFixedSize(1920 // 2, 1080 // 2)

        layout = QVBoxLayout()

        self.title = QLineEdit(self.todo.name)
        label_font = self.title.font()
        label_font.setPointSizeF(20)
        label_font.setBold(True)
        self.title.setFont(label_font)
        layout.addWidget(self.title)

        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Plain)
        layout.addWidget(horizontal_line)

        switch_layout = QHBoxLayout()
        description_label = QLabel("Description")
        label_font = description_label.font()
        label_font.setPointSizeF(20)
        label_font.setBold(True)
        description_label.setFont(label_font)
        switch_layout.addWidget(description_label, stretch=1)

        self.switch_raw = QPushButton("Raw")
        switch_layout.addWidget(self.switch_raw, alignment=Qt.AlignRight)
        self.switch_md = QPushButton("Markdown")
        switch_layout.addWidget(self.switch_md, alignment=Qt.AlignRight)

        layout.addLayout(switch_layout)

        self.stack = QStackedWidget()

        self.description_raw = QTextEdit()
        self.description_raw.setText(self.todo.description)
        self.description_md = QTextEdit()

        self.stack.addWidget(self.description_raw)
        self.stack.addWidget(self.description_md)

        layout.addWidget(self.stack)

        self.switch_raw.pressed.connect(self.switch)
        self.switch_md.pressed.connect(self.switch)

        self.button_done = QPushButton("Done")
        self.button_done.pressed.connect(self.accept)
        layout.addWidget(self.button_done)
        self.setLayout(layout)

    @pyqtSlot()
    def switch(self) -> None:
        button = self.sender()
        other_button = self.switch_raw if button == self.switch_md else self.switch_md
        self.stack.setCurrentIndex(0 if button == self.switch_raw else 1)

        button.setChecked(True)
        other_button.setChecked(False)

        if button == self.switch_raw:
            self.description_raw.setText(self.description_md.toMarkdown())
        else:
            self.description_md.setMarkdown(self.description_raw.toPlainText())

    def accept(self) -> None:
        self.todo.description = self.description_raw.toPlainText()
        self.todo.name = self.title.text()

        save_todos()
        super().accept()
