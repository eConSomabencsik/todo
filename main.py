from __future__ import annotations

from typing import List, Union

import keyboard
import qdarktheme

# pylint: disable = no-name-in-module
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)
from pyqt_custom_titlebar_window import CustomTitlebarWindow
from screeninfo import get_monitors

from handler import (
    add_todo,
    add_todo_list,
    delete_todo,
    delete_todo_list,
    mark_completed,
    read_todos,
)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Todos")

        for monitor in get_monitors():
            if not monitor.is_primary:
                continue
            window_x = (monitor.width // 2) - (WINDOW_WIDTH // 2)
            window_y = (monitor.height // 2) - (WINDOW_HEIGHT // 2)
            self.setGeometry(window_x, window_y, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.todos = read_todos()

        self.focus_on = False

        self.setup_ui()

        menu_bar = self.menuBar()
        file_menu = QMenu("&File", self)
        file_menu.addAction(
            QAction("&Exit", self, triggered=self.close, shortcut="Ctrl+Q")
        )
        menu_bar.addMenu(file_menu)

        edit_menu = QMenu("&Edit", self)
        edit_menu.addAction(
            QAction(
                "&Add Todo List", self, triggered=self.add_todo_list, shortcut="Ctrl+L"
            )
        )
        edit_menu.addAction(
            QAction("&Add Todo", self, triggered=self.add_todo, shortcut="Ctrl+A")
        )
        edit_menu.addAction(
            QAction(
                "&Delete Todo List",
                self,
                triggered=self.delete_todo_list,
                shortcut="Ctrl+D",
            )
        )
        menu_bar.addMenu(edit_menu)

        keyboard.on_press(self.keyboard_event)

    def setup_ui(self) -> None:
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        TodoWidget.objects = []
        TodoListWidget.objects = []
        for idx, todo_list in enumerate(self.todos):
            todo_list_widget = TodoListWidget(todo_list, self.todos[todo_list])
            main_layout.addWidget(todo_list_widget)

            if idx < len(self.todos) - 1:
                separator = QFrame()
                separator.setFrameShape(QFrame.VLine)
                separator.setFrameShadow(QFrame.Plain)
                main_layout.addWidget(separator)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def add_todo(self) -> None:
        todo_lists = list(self.todos.keys())
        AddTodoWidget(todo_lists).exec_()
        self.refresh_todos()

    def add_todo_list(self) -> None:
        addTodoListWidget().exec_()
        self.refresh_todos()

    def delete_todo_list(self) -> None:
        todo_lists = list(self.todos.keys())

        delete_window = QDialog()
        delete_todo_list_widget = QComboBox()
        delete_todo_list_widget.addItems(todo_lists)

        layout = QVBoxLayout()
        delete_window.setLayout(layout)

        title_label = QLabel("Delete a todo list")
        font = title_label.font()
        font.setPointSize(20)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Plain)
        layout.addWidget(separator)

        layout.addWidget(delete_todo_list_widget)

        delete_button = QPushButton("Delete")
        layout.addWidget(delete_button)

        delete_button.clicked.connect(delete_window.accept)

        if delete_window.exec_():
            todo_list = delete_todo_list_widget.currentText()
            delete_todo_list(todo_list)
            self.refresh_todos()

    def refresh_todos(self) -> None:
        layout = self.centralWidget().layout()
        self.delete_widgets_from_layout(layout)
        self.todos = read_todos()
        self.setup_ui()

    def delete_widgets_from_layout(
        self, layout: Union[QVBoxLayout, QHBoxLayout]
    ) -> None:
        for i in reversed(range(layout.count())):
            w = layout.itemAt(i).widget()
            if w is not None:
                w.deleteLater()
                w.setParent(None)
            try:
                l = layout.itemAt(i).layout()
            except AttributeError:
                continue
            if l is not None:
                self.delete_widgets_from_layout(l)

    def keyboard_event(self, event: keyboard.KeyboardEvent):
        if event.event_type != "down":
            return
        if event.name == "tab":
            if not self.focus_on:
                self.focus_on = True
                TodoWidget.objects[0].set_focused(True)
            else:
                self.focus_on = False
                for todo_widget in TodoWidget.objects:
                    todo_widget.set_focused(False)
        elif event.name == "space":
            for todo_widget in TodoWidget.objects:
                if todo_widget.is_focused:
                    todo_widget.completed_checkbox.setChecked(
                        not todo_widget.completed_checkbox.isChecked()
                    )
                    break
        elif event.name == "left":
            stop = False
            for todo_widget in TodoWidget.objects:
                if todo_widget.is_focused:
                    todo_widget.set_focused(False)

                    for idx, todo_list_widget in enumerate(TodoListWidget.objects):
                        if todo_list_widget.todo_list != todo_widget.todo_list:
                            continue

                        current_idx = 0
                        for todo_idx, todo in enumerate(todo_list_widget.todos):
                            if todo_widget.todo in todo:
                                current_idx = todo_idx
                                break

                        next_idx = idx - 1
                        if next_idx < 0:
                            next_idx = len(TodoListWidget.objects) - 1

                        if current_idx >= len(TodoListWidget.objects[next_idx].todos):
                            current_idx = (
                                len(TodoListWidget.objects[next_idx].todos) - 1
                            )

                        next_todo = TodoListWidget.objects[next_idx].todos[current_idx]
                        for next_todo_widget in TodoWidget.objects:
                            if next_todo_widget.todo in next_todo:
                                next_todo_widget.set_focused(True)
                                stop = True
                                break
                    if stop:
                        break
        elif event.name == "right":
            stop = False
            for todo_widget in TodoWidget.objects:
                if todo_widget.is_focused:
                    todo_widget.set_focused(False)

                    for idx, todo_list_widget in enumerate(TodoListWidget.objects):
                        if todo_list_widget.todo_list != todo_widget.todo_list:
                            continue

                        current_idx = 0
                        for todo_idx, todo in enumerate(todo_list_widget.todos):
                            if todo_widget.todo in todo:
                                current_idx = todo_idx
                                break

                        next_idx = idx + 1
                        if next_idx >= len(TodoListWidget.objects):
                            next_idx = 0

                        if current_idx >= len(TodoListWidget.objects[next_idx].todos):
                            current_idx = (
                                len(TodoListWidget.objects[next_idx].todos) - 1
                            )

                        next_todo = TodoListWidget.objects[next_idx].todos[current_idx]
                        for next_todo_widget in TodoWidget.objects:
                            if next_todo_widget.todo in next_todo:
                                next_todo_widget.set_focused(True)
                                stop = True
                                break
                    if stop:
                        break
        elif event.name == "up":
            stop = False
            for todo_widget in TodoWidget.objects:
                if todo_widget.is_focused:
                    todo_widget.set_focused(False)

                    for todo_list_widget in TodoListWidget.objects:
                        if todo_list_widget.todo_list != todo_widget.todo_list:
                            continue

                        for idx, todo in enumerate(todo_list_widget.todos):
                            if todo_widget.todo in todo:
                                current_idx = idx
                                break

                        next_idx = current_idx - 1
                        if next_idx < 0:
                            next_idx = len(todo_list_widget.todos) - 1

                        next_todo = todo_list_widget.todos[next_idx]
                        for next_todo_widget in TodoWidget.objects:
                            if next_todo_widget.todo in next_todo:
                                next_todo_widget.set_focused(True)
                                stop = True
                                break
                if stop:
                    break
        elif event.name == "down":
            stop = False
            for todo_widget in TodoWidget.objects:
                if todo_widget.is_focused:
                    todo_widget.set_focused(False)

                    for todo_list_widget in TodoListWidget.objects:
                        if todo_list_widget.todo_list != todo_widget.todo_list:
                            continue

                        for idx, todo in enumerate(todo_list_widget.todos):
                            if todo_widget.todo in todo:
                                current_idx = idx
                                break

                        next_idx = current_idx + 1
                        if next_idx >= len(todo_list_widget.todos):
                            next_idx = 0

                        next_todo = todo_list_widget.todos[next_idx]
                        for next_todo_widget in TodoWidget.objects:
                            if next_todo_widget.todo in next_todo:
                                next_todo_widget.set_focused(True)
                                stop = True
                                break
                if stop:
                    break


class TodoWidget(QWidget):

    objects: List[TodoWidget] = []

    deleted = pyqtSignal()
    focused = pyqtSignal(bool)

    def __init__(self, todo_list: str, todo: str, completed: bool = False):
        super().__init__()
        self.todo_list = todo_list
        self.todo = todo
        self.completed = completed

        self.is_focused = False

        self.setup_ui()

        TodoWidget.objects.append(self)

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.todo_label = QLabel(self.todo)
        if self.completed:
            self.todo_label.setStyleSheet("text-decoration: line-through;")
        font = self.todo_label.font()
        font.setPointSize(12)
        self.todo_label.setFont(font)
        layout.addWidget(self.todo_label)

        self.completed_checkbox = QCheckBox("Completed")
        self.completed_checkbox.setChecked(self.completed)
        self.completed_checkbox.stateChanged.connect(self.mark_completed)
        self.completed_checkbox.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(self.completed_checkbox)

        self.delete_button = QPushButton("Delete")
        self.delete_button.pressed.connect(self.delete)
        self.delete_button.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(self.delete_button)

    def delete(self) -> None:
        delete_todo(self.todo_list, self.todo)
        self.deleteLater()
        self.deleted.emit()

    def mark_completed(self) -> None:
        mark_completed(self.todo_list, self.todo, self.completed_checkbox.isChecked())
        self.todo_label.setStyleSheet(
            "text-decoration: line-through;"
            if self.completed_checkbox.isChecked()
            else ""
        )

    def set_focused(self, focused: bool) -> None:
        self.is_focused = focused
        self.setStyleSheet("background-color: #606060;" if focused else "")


class TodoListWidget(QWidget):

    objects: List[TodoListWidget] = []

    def __init__(self, todo_list: str, todos: List[str]):
        super().__init__()
        self.todo_list = todo_list
        self.todos = todos

        self.setup_ui()

        TodoListWidget.objects.append(self)

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel(self.todo_list)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Plain)
        layout.addWidget(separator)

        for todo in self.todos:
            completed = False
            if " (Completed)" in todo:
                completed = True
                todo = todo.replace(" (Completed)", "")
            todo_widget = TodoWidget(self.todo_list, todo, completed)
            layout.addWidget(todo_widget)

            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Plain)
            layout.addWidget(separator)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)


class AddTodoWidget(QDialog):
    def __init__(self, todo_lists: List[str]):
        super().__init__()
        self.todo_lists = todo_lists

        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("Add a new todo")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Plain)
        layout.addWidget(separator)

        self.todo_list = QComboBox()
        self.todo_list.addItems(self.todo_lists)
        layout.addWidget(self.todo_list)

        self.todo_input = QLabel("Todo:")
        layout.addWidget(self.todo_input)

        self.todo_input = QLineEdit()
        layout.addWidget(self.todo_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_todo)
        layout.addWidget(self.add_button)

    def add_todo(self) -> None:
        todo_list = self.todo_list.currentText()
        todo = self.todo_input.text()
        add_todo(todo_list, todo)
        self.close()


class addTodoListWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("Add a new todo list")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Plain)
        layout.addWidget(separator)

        self.todo_list_input = QLineEdit()
        layout.addWidget(self.todo_list_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_todo_list)
        layout.addWidget(self.add_button)

    def add_todo_list(self) -> None:
        todo_list = self.todo_list_input.text()
        add_todo_list(todo_list)
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    qdarktheme.setup_theme()
    window = CustomTitlebarWindow(MainWindow())
    # window.setMenuAsTitleBar()
    # window.setButtons()
    window.showMaximized()
    app.exec_()
