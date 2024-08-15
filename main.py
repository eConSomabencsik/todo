from __future__ import annotations

import sys

import qdarktheme
from PyQt5.QtWidgets import QApplication
from pyqt_custom_titlebar_window import CustomTitlebarWindow

if __name__ == "__main__":
    from tda.view.main_window import MainWindow

    qdarktheme.enable_hi_dpi()

    app = QApplication(sys.argv)
    qdarktheme.setup_theme("dark")
    window = CustomTitlebarWindow(MainWindow())
    window.setButtons()
    window.showMaximized()
    sys.exit(app.exec_())
