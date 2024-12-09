import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QMenuBar, QAction, QFileDialog, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont, QIcon
from fpdf import FPDF

class Notebook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"  # Current theme, default is light
        self.init_ui()

    def init_ui(self):
        """
        Initializes the main user interface.
        Sets up the main window, text area, and menu bar.
        """
        # Set main window properties
        self.setWindowTitle("Notebook")
        self.setGeometry(100, 100, 800, 600)

        # Create and set text area
        self.text_area = QTextEdit(self)
        self.text_area.setFont(QFont("Arial", 14))
        self.setCentralWidget(self.text_area)

        # Apply the default theme
        self.apply_css("styles/light.css")

        # Create menu bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Set up menus and actions
        self.create_menus()