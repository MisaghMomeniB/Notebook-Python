import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenuBar, QAction, QFileDialog, QMessageBox, QInputDialog, QFontDialog
from PyQt5.QtGui import QFont, QIcon
from fpdf import FPDF
from PyQt5.QtCore import QSettings

# Main Notebook application class
class Notebook(QMainWindow):
    def __init__(self):
        # Initialize the base QMainWindow class
        super().__init__()
        
        # Initial theme setup, default is "light"
        self.current_theme = "light"
        
        # Create a QSettings instance to manage app settings
        self.settings = QSettings("MyCompany", "NotebookApp")
        
        # Create a QTextEdit widget for the main text area
        self.text_area = QTextEdit(self)
        self.text_area.setFont(QFont("Arial", 14))  # Set the default font to Arial with size 14
        
        # Set the text area as the central widget of the main window
        self.setCentralWidget(self.text_area)
        
        # Initialize the user interface (UI)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components for the notebook application."""
        
        # Set the window title
        self.setWindowTitle("Notebook")
        
        # Set the window geometry (position and size)
        self.setGeometry(100, 100, 800, 600)
        
        # Load the theme (either light or dark) from settings
        self.load_theme()
        
        # Create the menus for the application
        self.create_menus()

    def load_theme(self):
        """Load the theme (light or dark) from the application settings."""
        
        # Get the current theme path from settings or default to light theme
        theme = self.settings.value("theme", "styles/light.css")
        
        # Apply the CSS stylesheet based on the selected theme
        self.apply_css(theme)

    def apply_css(self, css_file):
        """Apply a CSS file as the application's stylesheet."""
        try:
            # Open and read the CSS file
            with open(css_file, "r") as file:
                self.setStyleSheet(file.read())  # Apply the CSS to the application
        except Exception as e:
            # If there is an error loading the CSS file, show an error message
            self.show_error("Error", f"Could not load stylesheet: {e}")

    def create_menus(self):
        """Create the menus for the notebook application."""
        
        # Dictionary defining the menu structure and actions
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

        # Create a menu bar
        self.menu_bar = self.menuBar()
        
        # Loop through the menu data to create menus and actions
        for menu_name, actions in menu_data.items():
            # Create a new menu with the name from the menu_data dictionary
            menu = self.menu_bar.addMenu(menu_name)
            
            # Loop through each action in the current menu
            for action_name, icon_path, handler in actions:
                # Set the icon if provided, otherwise use a default icon
                icon = QIcon(icon_path) if icon_path else QIcon()
                
                # Create an action with the specified icon, name, and handler
                action = QAction(icon, action_name, self)
                
                # Connect the action to the handler (function)
                action.triggered.connect(handler)
                
                # Add the action to the menu
                menu.addAction(action)

    def new_file(self):
        """Clear the text area (create a new file)."""
        self.text_area.clear()

    def open_file(self):
        """Open a file and load its content into the text area."""
        # Open a file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        
        # If a file is selected, load its content
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        """Load the content from the selected file into the text area."""
        try:
            # Open the file in read mode and set its content to the text area
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area.setText(file.read())
        except Exception as e:
            # If an error occurs (e.g., file not found), show an error message
            self.show_error("Error", f"Could not open file: {e}")

    def save_file(self):
        """Save the content of the text area to a file."""
        # Open a file dialog to specify the save location
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        
        # If a file path is selected, save the content
        if file_path:
            self.save_to_file(file_path)

    def save_to_file(self, file_path):
        """Save the text area content to a specified file."""
        try:
            # Open the file in write mode and save the text area content
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.toPlainText())
        except Exception as e:
            # Show an error message if saving the file fails
            self.show_error("Error", f"Could not save file: {e}")

    def export_to_pdf(self):
        """Export the content of the text area to a PDF file."""
        # Open a file dialog to specify the save location for the PDF
        file_path, _ = QFileDialog.getSaveFileName(self, "Export to PDF", "", "PDF Files (*.pdf);;All Files (*)")
        
        # If a file path is selected, generate the PDF
        if file_path:
            self.create_pdf(file_path)

    def create_pdf(self, file_path):
        """Create a PDF document from the text area content and save it."""
        try:
            # Create an instance of the FPDF class
            pdf = FPDF()
            
            # Add a new page to the PDF
            pdf.add_page()
            
            # Set the font for the PDF
            pdf.set_font("Arial", size=12)
            
            # Loop through each line of the text area content and add it to the PDF
            for line in self.text_area.toPlainText().split('\n'):
                pdf.cell(0, 10, line, ln=True)
            
            # Output the PDF to the specified file path
            pdf.output(file_path)
        except Exception as e:
            # Show an error message if there is an issue exporting to PDF
            self.show_error("Error", f"Could not export to PDF: {e}")

    def find_text(self):
        """Find and highlight specific text in the text area."""
        # Open an input dialog to get the text to search for
        search_text, ok = QInputDialog.getText(self, "Find Text", "Enter text to search:")
        
        # If the user entered search text and confirmed, perform the search
        if ok and search_text:
            cursor = self.text_area.textCursor()
            
            # Search for the text and update the cursor position
            cursor = self.text_area.document().find(search_text, cursor)
            
            # If the text is not found, show an information message
            if cursor.isNull():
                QMessageBox.information(self, "Find", "Text not found!")
            else:
                # Otherwise, set the text cursor to the found position
                self.text_area.setTextCursor(cursor)

    def change_font_dialog(self):
        """Open a dialog to allow the user to change the font."""
        # Open the font dialog to allow the user to select a new font
        font, ok = QFontDialog.getFont()
        
        # If the user selected a font, apply it to the text area
        if ok:
            self.text_area.setFont(font)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        # Switch between themes and update the CSS accordingly
        new_theme = "styles/dark.css" if self.current_theme == "light" else "styles/light.css"
        
        # Apply the new theme and save it in settings
        self.apply_css(new_theme)
        self.settings.setValue("theme", new_theme)
        
        # Update the current theme status
        self.current_theme = "dark" if self.current_theme == "light" else "light"

    def show_error(self, title, message):
        """Show an error message in a dialog."""
        QMessageBox.critical(self, title, message)

# Application entry point
if __name__ == "__main__":
    # Create the application instance
    app = QApplication(sys.argv)
    
    # Create the notebook window instance
    notebook = Notebook()
    
    # Show the notebook window
    notebook.show()
    
    # Start the application's event loop
    sys.exit(app.exec_())