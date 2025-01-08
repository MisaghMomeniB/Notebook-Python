import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenuBar, QAction, QFileDialog, QMessageBox, QInputDialog, QFontDialog
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSettings
from fpdf import FPDF

class Notebook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self.settings = QSettings("MyCompany", "NotebookApp")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Notebook")
        self.setGeometry(100, 100, 800, 600)
        self.text_area = QTextEdit(self)
        self.text_area.setFont(QFont("Arial", 14))
        self.setCentralWidget(self.text_area)
        self.apply_css(self.settings.value("theme", "styles/light.css"))
        self.create_menus()

    def create_menus(self):
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        file_menu = self.menu_bar.addMenu("File")
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
        file_menu.addActions([new_action, open_action, save_action, export_pdf_action])
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        edit_menu = self.menu_bar.addMenu("Edit")
        find_action = QAction("Find...", self)
        find_action.triggered.connect(self.find_text)
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.text_area.undo)
        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.text_area.redo)
        edit_menu.addActions([find_action, undo_action, redo_action])

        view_menu = self.menu_bar.addMenu("View")
        toggle_theme_action = QAction("Toggle Theme", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(toggle_theme_action)

        font_menu = self.menu_bar.addMenu("Font")
        change_font_action = QAction("Change Font", self)
        change_font_action.triggered.connect(self.change_font_dialog)
        font_menu.addAction(change_font_action)

    def apply_css(self, css_file):
        try:
            with open(css_file, "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load stylesheet:\n{e}")

    def new_file(self):
        self.text_area.clear()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_area.setText(file.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")

    def export_to_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export to PDF", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for line in self.text_area.toPlainText().split('\n'):
                    pdf.cell(0, 10, line, ln=True)
                pdf.output(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not export to PDF:\n{e}")

    def find_text(self):
        search_text, ok = QInputDialog.getText(self, "Find Text", "Enter text to search:")
        if ok and search_text:
            cursor = self.text_area.textCursor()
            cursor = self.text_area.document().find(search_text, cursor)
            if cursor.isNull():
                QMessageBox.information(self, "Find", "Text not found!")
            else:
                self.text_area.setTextCursor(cursor)

    def change_font_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_area.setFont(font)

    def toggle_theme(self):
        if self.current_theme == "light":
            self.apply_css("styles/dark.css")
            self.settings.setValue("theme", "styles/dark.css")
            self.current_theme = "dark"
        else:
            self.apply_css("styles/light.css")
            self.settings.setValue("theme", "styles/light.css")
            self.current_theme = "light"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notebook = Notebook()
    notebook.show()
    sys.exit(app.exec_())