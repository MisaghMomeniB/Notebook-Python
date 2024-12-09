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
        
    def apply_css(self, css_file):
        """
        Applies a CSS file to the application.

        Args:
            css_file (str): Path to the CSS file.
        """
        try:
            with open(css_file, "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load stylesheet:\n{e}")
            
    def new_file(self):
        """
        Clears the text area for a new file.
        """
        self.text_area.clear()

    def open_file(self):
        """
        Opens a text file and displays its content in the text area.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.text_area.setText(content)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")

    def save_file(self):
        """
        Saves the content of the text area to a file.
        """
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.toPlainText())
                QMessageBox.information(self, "Success", "File saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")

    def export_to_pdf(self):
        """
        Exports the content of the text area to a PDF file.
        """
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export to PDF", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                lines = self.text_area.toPlainText().split('\n')
                for line in lines:
                    pdf.cell(0, 10, line, ln=True)
                pdf.output(file_path)
                QMessageBox.information(self, "Success", "PDF exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not export to PDF:\n{e}")
                
    def find_text(self):
        """
        Finds a specific text in the text area.
        """
        search_text, ok = QInputDialog.getText(self, "Find Text", "Enter text to search:")
        if ok and search_text:
            cursor = self.text_area.textCursor()
            cursor = self.text_area.document().find(search_text, cursor)
            if cursor.isNull():
                QMessageBox.information(self, "Find", "Text not found!")
            else:
                self.text_area.setTextCursor(cursor)

    def change_font(self):
        """
        Changes the text area's font to Courier.
        """
        self.text_area.setFont(QFont("Courier", 14))

    def toggle_theme(self):
        """
        Toggles between light and dark themes.
        """
        if self.current_theme == "light":
            self.apply_css("styles/dark.css")
            self.current_theme = "dark"
        else:
            self.apply_css("styles/light.css")
            self.current_theme = "light"