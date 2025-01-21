import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenuBar, QAction, QFileDialog, QMessageBox, QInputDialog, QFontDialog
from PyQt5.QtGui import QFont, QIcon
from fpdf import FPDF
from PyQt5.QtCore import QSettings

class Notebook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self.settings = QSettings("MyCompany", "NotebookApp")
        self.text_area = QTextEdit(self)
        self.text_area.setFont(QFont("Arial", 14))
        self.setCentralWidget(self.text_area)
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Notebook")
        self.setGeometry(100, 100, 800, 600)

        # Load theme from settings
        self.apply_css(self.settings.value("theme", "styles/light.css"))

        # Create menus
        self.create_menus()

    def create_menus(self):
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

        self.menu_bar = self.menuBar()
        for menu_name, actions in menu_data.items():
            menu = self.menu_bar.addMenu(menu_name)
            for action_name, icon_path, handler in actions:
                icon = QIcon(icon_path) if icon_path else QIcon()
                action = QAction(icon, action_name, self)
                action.triggered.connect(handler)
                menu.addAction(action)

    def apply_css(self, css_file):
        """Apply CSS stylesheet."""
        try:
            with open(css_file, "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            self.show_error("Error", f"Could not load stylesheet: {e}")

    def new_file(self):
        """Clear text area."""
        self.text_area.clear()

    def open_file(self):
        """Open a file and load its content."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        """Load content from the specified file."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area.setText(file.read())
        except Exception as e:
            self.show_error("Error", f"Could not open file: {e}")

    def save_file(self):
        """Save the text area content to a file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.save_to_file(file_path)

    def save_to_file(self, file_path):
        """Save content to the specified file."""
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.toPlainText())
        except Exception as e:
            self.show_error("Error", f"Could not save file: {e}")

    def export_to_pdf(self):
        """Export content to a PDF file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Export to PDF", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            self.create_pdf(file_path)

    def create_pdf(self, file_path):
        """Create and save a PDF from text area content."""
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
        """Find text in the text area."""
        search_text, ok = QInputDialog.getText(self, "Find Text", "Enter text to search:")
        if ok and search_text:
            cursor = self.text_area.textCursor()
            cursor = self.text_area.document().find(search_text, cursor)
            if cursor.isNull():
                QMessageBox.information(self, "Find", "Text not found!")
            else:
                self.text_area.setTextCursor(cursor)

    def change_font_dialog(self):
        """Open font selection dialog."""
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_area.setFont(font)

    def toggle_theme(self):
        """Toggle between light and dark theme."""
        if self.current_theme == "light":
            self.apply_css("styles/dark.css")
            self.settings.setValue("theme", "styles/dark.css")
            self.current_theme = "dark"
        else:
            self.apply_css("styles/light.css")
            self.settings.setValue("theme", "styles/light.css")
            self.current_theme = "light"

    def show_error(self, title, message):
        """Show an error message in a dialog."""
        QMessageBox.critical(self, title, message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notebook = Notebook()
    notebook.show()
    sys.exit(app.exec_())