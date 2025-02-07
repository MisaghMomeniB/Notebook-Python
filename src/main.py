import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenuBar, QAction, QFileDialog, QMessageBox, QInputDialog, QFontDialog
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSettings
from fpdf import FPDF

# Main Notebook application class
class Notebook(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize settings
        self.settings = QSettings("MyCompany", "NotebookApp")
        
        # Default font and theme setup
        self.current_theme = "light"
        self.text_area = QTextEdit(self)
        self.text_area.setFont(QFont("Arial", 14))
        self.setCentralWidget(self.text_area)
        
        # Initialize UI
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Notebook")
        self.setGeometry(100, 100, 800, 600)
        self.load_theme()
        self.create_menus()

    def load_theme(self):
        """Load the current theme from settings."""
        theme = self.settings.value("theme", "styles/light.css")
        self.apply_css(theme)

    def apply_css(self, css_file):
        """Apply a CSS file as the application's stylesheet."""
        try:
            with open(css_file, "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            self.show_error("Error", f"Could not load stylesheet: {e}")

    def create_menus(self):
        """Create the menu bar and actions."""
        menu_data = {
            "File": [
                ("New", "icons/new.png", self.new_file),
                ("Open...", "icons/open.png", self.open_file),
                ("Save...", "icons/save.png", self.save_file),
                ("Export to PDF...", "icons/pdf.png", self.export_to_pdf),
                ("Exit", None, self.close),
            ],
            "Edit": [
                ("Find...", None, self.find_text),
                ("Undo", None, self.text_area.undo),
                ("Redo", None, self.text_area.redo),
            ],
            "View": [
                ("Toggle Theme", None, self.toggle_theme),
            ],
            "Font": [
                ("Change Font", None, self.change_font_dialog),
            ]
        }

        menu_bar = self.menuBar()
        for menu_name, actions in menu_data.items():
            menu = menu_bar.addMenu(menu_name)
            for action_name, icon_path, handler in actions:
                icon = QIcon(icon_path) if icon_path else QIcon()
                action = QAction(icon, action_name, self)
                action.triggered.connect(handler)
                menu.addAction(action)

    def new_file(self):
        """Clear the text area (create a new file)."""
        self.text_area.clear()

    def open_file(self):
        """Open a file and load its content into the text area."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        """Load file content into the text area."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area.setText(file.read())
        except Exception as e:
            self.show_error("Error", f"Could not open file: {e}")

    def save_file(self):
        """Save the content of the text area to a file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.save_to_file(file_path)

    def save_to_file(self, file_path):
        """Save text area content to a specified file."""
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.toPlainText())
        except Exception as e:
            self.show_error("Error", f"Could not save file: {e}")

    def export_to_pdf(self):
        """Export the content of the text area to a PDF file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Export to PDF", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            self.create_pdf(file_path)

    def create_pdf(self, file_path):
        """Create a PDF document from the text area content."""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in self.text_area.toPlainText().split('\n'):
                pdf.cell(0, 10, line, ln=True)
            pdf.output(file_path)
        except Exception as e:
            self.show_error("Error", f"Could not export to PDF: {e}")

    def find_text(self):
        """Find and highlight specific text in the text area."""
        search_text, ok = QInputDialog.getText(self, "Find Text", "Enter text to search:")
        if ok and search_text:
            cursor = self.text_area.document().find(search_text)
            if cursor.isNull():
                QMessageBox.information(self, "Find", "Text not found!")
            else:
                self.text_area.setTextCursor(cursor)

    def change_font_dialog(self):
        """Open a dialog to allow the user to change the font."""
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_area.setFont(font)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        new_theme = "styles/dark.css" if self.current_theme == "light" else "styles/light.css"
        self.apply_css(new_theme)
        self.settings.setValue("theme", new_theme)
        self.current_theme = "dark" if self.current_theme == "light" else "light"

    def show_error(self, title, message):
        """Show an error message in a dialog."""
        QMessageBox.critical(self, title, message)

# Application entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    notebook = Notebook()
    notebook.show()
    sys.exit(app.exec_())