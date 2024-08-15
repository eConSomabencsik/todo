from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QShortcut,
    QWidget,
)

from tda.control import json_handler
from tda.view.dialogs.add_todo import AddTodoDialog
from tda.view.dialogs.add_todo_list import AddTodoListDialog
from tda.view.dialogs.delete_todo_list import DeleteTodoList
from tda.view.widgets.todo_list_widget import TodoListWidget
from tda.view.widgets.todo_widget import TodoWidget


class MainWindow(QMainWindow):
    def __create_menu_bar(self) -> None:
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

    def __create_shortcuts(self) -> None:
        # Tab key is not caught in 'keyPressEvent' needed to create this shortcut
        tab_shortcut = QShortcut(QKeySequence(Qt.Key_Tab), self)
        tab_shortcut.activated.connect(partial(self.key_press, "Tab"))

        right_shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        right_shortcut.activated.connect(partial(self.key_press, "Right"))

        left_shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        left_shortcut.activated.connect(partial(self.key_press, "Left"))

        up_shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        up_shortcut.activated.connect(partial(self.key_press, "Up"))

        down_shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        down_shortcut.activated.connect(partial(self.key_press, "Down"))

        space_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self)
        space_shortcut.activated.connect(partial(self.key_press, "Space"))

    def __init__(self) -> None:
        super().__init__()
        self.__create_menu_bar()
        self.__create_shortcuts()
        self.setup_ui()

    def setup_ui(self) -> None:
        json_handler.read_todos()

        main_widget = QWidget(self)
        layout = self.create_base_view(main_widget)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def create_base_view(self, widget: QWidget) -> QHBoxLayout:
        layout = QHBoxLayout(widget)

        TodoListWidget.objects = []
        TodoWidget.objects = []
        for todo_list in json_handler.get_todo_lists():
            todo_list_widget = TodoListWidget(widget, todo_list)
            todo_list_widget.refresh.connect(self.setup_ui)
            layout.addWidget(todo_list_widget)

            separator = QFrame(widget)
            separator.setFrameShape(QFrame.VLine)
            separator.setFrameShadow(QFrame.Plain)

            layout.addWidget(separator)

        return layout

    def add_todo(self) -> None:
        add_todo_dialog = AddTodoDialog(self)
        if add_todo_dialog.exec_():
            json_handler.save_todos()
            self.setup_ui()

    def add_todo_list(self) -> None:
        add_todo_list_dialog = AddTodoListDialog(self)
        if add_todo_list_dialog.exec_():
            json_handler.save_todos()
            self.setup_ui()

    def delete_todo_list(self) -> None:
        delete_todo_list = DeleteTodoList(self)
        if delete_todo_list.exec_():
            self.setup_ui()

    def key_press(self, key: str) -> None:
        current_focused_todo = None
        current_todo_list = None
        first_todo_widget = None

        for todo_list in TodoListWidget.objects:
            for todo in TodoWidget.objects:
                if todo.parent() != todo_list:
                    continue
                if todo.has_focus:
                    current_focused_todo = todo
                    current_todo_list = todo_list
                    break
                if first_todo_widget is None:
                    first_todo_widget = todo

        if key == "Tab":
            if current_focused_todo is not None:
                current_focused_todo.set_focus(not current_focused_todo.has_focus)
            else:
                first_todo_widget.set_focus(True)

        if current_focused_todo is None:
            return

        if key == "Space":
            current_focused_todo.check_completed.setChecked(
                not current_focused_todo.check_completed.isChecked()
            )
            return

        current_widget_idx = current_todo_list.todo_widgets.index(current_focused_todo)
        current_list_widget_idx = TodoListWidget.objects.index(current_todo_list)

        if key == "Right":
            current_list_widget_idx += 1

            if current_list_widget_idx >= len(TodoListWidget.objects):
                current_list_widget_idx = 0

            if current_widget_idx >= len(
                TodoListWidget.objects[current_list_widget_idx].todo_widgets
            ):
                current_widget_idx = (
                    len(TodoListWidget.objects[current_list_widget_idx].todo_widgets)
                    - 1
                )

            current_focused_todo.set_focus(False)
            TodoListWidget.objects[current_list_widget_idx].todo_widgets[
                current_widget_idx
            ].set_focus(True)
        elif key == "Left":
            current_list_widget_idx -= 1

            if current_list_widget_idx >= len(TodoListWidget.objects):
                current_list_widget_idx = 0

            if current_widget_idx >= len(
                TodoListWidget.objects[current_list_widget_idx].todo_widgets
            ):
                current_widget_idx = (
                    len(TodoListWidget.objects[current_list_widget_idx].todo_widgets)
                    - 1
                )

            current_focused_todo.set_focus(False)
            TodoListWidget.objects[current_list_widget_idx].todo_widgets[
                current_widget_idx
            ].set_focus(True)
        elif key == "Up":
            current_widget_idx -= 1

            if current_widget_idx >= len(current_todo_list.todo_widgets):
                current_widget_idx = len(current_todo_list.todo_widgets) - 1

            current_focused_todo.set_focus(False)
            current_todo_list.todo_widgets[current_widget_idx].set_focus(True)
        elif key == "Down":
            current_widget_idx += 1

            if current_widget_idx >= len(current_todo_list.todo_widgets):
                current_widget_idx = 0

            current_focused_todo.set_focus(False)
            current_todo_list.todo_widgets[current_widget_idx].set_focus(True)
