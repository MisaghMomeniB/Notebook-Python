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
        
    def create_menus(self):
        """
        Creates the menu bar and adds actions to the menus.
        """
        # File menu
        file_menu = self.menu_bar.addMenu("File")

        # File menu actions
        new_action = QAction(QIcon("icons/new.png"), "New", self)
        new_action.triggered.connect(self.new_file)

        open_action = QAction(QIcon("icons/open.png"), "Open...", self)
        open_action.triggered.connect(self.open_file)

        save_action = QAction(QIcon("icons/save.png"), "Save...", self)
        save_action.triggered.connect(self.save_file)

        export_pdf_action = QAction(QIcon("icons/pdf.png"), "Export to PDF...", self)
        export_pdf_action.triggered.connect(self.export_to_pdf)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        # Add actions to the File menu
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(export_pdf_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = self.menu_bar.addMenu("Edit")

        # Edit menu actions
        find_action = QAction("Find...", self)
        find_action.triggered.connect(self.find_text)

        # Add actions to the Edit menu
        edit_menu.addAction(find_action)

        # View menu
        view_menu = self.menu_bar.addMenu("View")

        # View menu actions
        toggle_theme_action = QAction("Toggle Theme", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)

        # Add actions to the View menu
        view_menu.addAction(toggle_theme_action)

        # Font menu
        font_menu = self.menu_bar.addMenu("Font")

        # Font menu actions
        change_font_action = QAction("Change to Courier", self)
        change_font_action.triggered.connect(self.change_font)

        # Add actions to the Font menu
        font_menu.addAction(change_font_action)