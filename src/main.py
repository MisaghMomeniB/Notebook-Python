import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QMenuBar, QAction, QFileDialog,
    QMessageBox, QInputDialog, QFontDialog, QToolBar, QTabWidget, QWidget
)
from PyQt5.QtGui import QFont, QIcon, QTextCursor, QTextCharFormat
from PyQt5.QtCore import QSettings, QTimer
from fpdf import FPDF


class TextEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Arial", 14))
        self.file_path = None
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(300000)  # Auto-save every 5 minutes

    def auto_save(self):
        if self.file_path:
            try:
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(self.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, "Auto-Save Error", str(e))


class Notebook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("MyCompany", "NotebookApp")
        self.current_theme = "light"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Notebook")
        self.setGeometry(100, 100, 800, 600)
        self.load_theme()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.new_tab()

        self.create_menus()
        self.create_toolbar()

    def new_tab(self):
        editor = TextEditor()
        index = self.tabs.addTab(editor, "Untitled")
        self.tabs.setCurrentIndex(index)

    def current_editor(self):
        return self.tabs.currentWidget()

    def load_theme(self):
        theme = self.settings.value("theme", "styles/light.css")
        self.apply_css(theme)

    def apply_css(self, css_file):
        try:
            with open(css_file, "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            QMessageBox.critical(self, "Theme Error", f"Could not load theme: {e}")

    def create_menus(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("New", self.new_tab)
        file_menu.addAction("Open...", self.open_file)
        file_menu.addAction("Save...", self.save_file)
        file_menu.addAction("Export to PDF...", self.export_to_pdf)
        file_menu.addAction("Exit", self.close)

        # Edit Menu
        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction("Find...", self.find_text)
        edit_menu.addAction("Undo", lambda: self.current_editor().undo())
        edit_menu.addAction("Redo", lambda: self.current_editor().redo())

        # View Menu
        view_menu = menu_bar.addMenu("View")
        view_menu.addAction("Toggle Theme", self.toggle_theme)

        # Font Menu
        font_menu = menu_bar.addMenu("Font")
        font_menu.addAction("Change Font", self.change_font_dialog)

    def create_toolbar(self):
        toolbar = QToolBar("Formatting")
        self.addToolBar(toolbar)

        bold_action = QAction("Bold", self)
        bold_action.triggered.connect(self.toggle_bold)
        toolbar.addAction(bold_action)

        italic_action = QAction("Italic", self)
        italic_action.triggered.connect(self.toggle_italic)
        toolbar.addAction(italic_action)

        underline_action = QAction("Underline", self)
        underline_action.triggered.connect(self.toggle_underline)
        toolbar.addAction(underline_action)

    def toggle_bold(self):
        editor = self.current_editor()
        fmt = QTextCharFormat()
        weight = QFont.Bold if editor.fontWeight() != QFont.Bold else QFont.Normal
        fmt.setFontWeight(weight)
        editor.mergeCurrentCharFormat(fmt)

    def toggle_italic(self):
        editor = self.current_editor()
        fmt = QTextCharFormat()
        fmt.setFontItalic(not editor.fontItalic())
        editor.mergeCurrentCharFormat(fmt)

    def toggle_underline(self):
        editor = self.current_editor()
        fmt = QTextCharFormat()
        fmt.setFontUnderline(not editor.fontUnderline())
        editor.mergeCurrentCharFormat(fmt)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    editor = TextEditor()
                    editor.setText(file.read())
                    editor.file_path = file_path
                    index = self.tabs.addTab(editor, file_path.split("/")[-1])
                    self.tabs.setCurrentIndex(index)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {e}")

    def save_file(self):
        editor = self.current_editor()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(editor.toPlainText())
                editor.file_path = file_path
                self.tabs.setTabText(self.tabs.currentIndex(), file_path.split("/")[-1])
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

    def export_to_pdf(self):
        from fpdf import FPDF
        file_path, _ = QFileDialog.getSaveFileName(self, "Export to PDF", "", "PDF Files (*.pdf)")
        if file_path:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for line in self.current_editor().toPlainText().split("\n"):
                    pdf.cell(200, 10, line.encode("latin-1", "replace").decode("latin-1"), ln=True)
                pdf.output(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"PDF export failed: {e}")

    def find_text(self):
        editor = self.current_editor()
        search_text, ok = QInputDialog.getText(self, "Find Text", "Enter text to search:")
        if ok and search_text:
            cursor = editor.textCursor()
            format = QTextCharFormat()
            format.setBackground(Qt.yellow)
            editor.moveCursor(QTextCursor.Start)
            while editor.find(search_text):
                cursor = editor.textCursor()
                cursor.mergeCharFormat(format)

    def change_font_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.current_editor().setFont(font)

    def toggle_theme(self):
        new_theme = "styles/dark.css" if self.current_theme == "light" else "styles/light.css"
        self.apply_css(new_theme)
        self.settings.setValue("theme", new_theme)
        self.current_theme = "dark" if self.current_theme == "light" else "light"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Notebook()
    window.show()
    sys.exit(app.exec_())