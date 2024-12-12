# 📒 Notebook App

A simple and versatile text editor built with Python using the **PyQt5** framework. This application allows users to create, edit, save, and export text files as PDFs, with support for customizable themes and fonts.

## 🖥️ Features

- **Create New File**: Start with a blank document. ✍️
- **Open File**: Open and edit existing text files. 📂
- **Save File**: Save your work to your preferred location. 💾
- **Export to PDF**: Export your document as a PDF file. 📄➡️📑
- **Find Text**: Search for specific text within your document. 🔍
- **Toggle Themes**: Switch between light and dark themes for better readability. 🌞🌙
- **Change Font**: Change the text font to Courier for better legibility. 🔤

## ⚙️ Requirements

To run this project, you need Python installed on your system along with the following packages:

- `PyQt5` – GUI toolkit for Python
- `fpdf` – Library to generate PDFs

You can install the required dependencies using `pip`:

```bash
pip install PyQt5 fpdf
```

## 🛠️ Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/notebook-app.git
   cd notebook-app
   ```

2. **Install dependencies**:
   ```bash
   pip install PyQt5 fpdf
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 📝 Usage

Once you launch the app, you’ll have the following options:

1. **Create a new file**: Select `File > New` to clear the current document and start fresh.
2. **Open an existing file**: Select `File > Open...` to load a text file into the editor.
3. **Save your file**: Select `File > Save...` to save your work.
4. **Export to PDF**: Select `File > Export to PDF...` to save the content of your document as a PDF.
5. **Search for text**: Select `Edit > Find...` to search for specific text in your document.
6. **Change font**: Select `Font > Change to Courier` to update the text font.
7. **Toggle theme**: Select `View > Toggle Theme` to switch between light and dark themes.

## 🎨 Themes

The app supports both **light** and **dark** themes. You can easily switch between them via the "View" menu. Your current theme is saved during the session, making it simple to pick up where you left off.

## 🐛 Troubleshooting

If you encounter any issues, such as the application not starting, ensure that all dependencies are correctly installed. If you face issues with loading or saving files, verify that you have proper permissions for the directories you are working with.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

### 1. Importing Modules
```python
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QMenuBar, QAction, QFileDialog, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont, QIcon
from fpdf import FPDF
```
- `sys`: Provides access to some variables used or maintained by the Python interpreter.
- `PyQt5.QtWidgets`: Imports various widgets from PyQt5 to build the graphical interface (like windows, text areas, menus, etc.).
- `QFont`, `QIcon`: These classes are used to set fonts and icons for GUI elements.
- `FPDF`: A library for generating PDF documents in Python.

### 2. The Notebook Class
```python
class Notebook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"  # Current theme, default is light
        self.init_ui()
```
- `Notebook`: This class inherits from `QMainWindow`, making it a window-based application.
- `self.current_theme`: Keeps track of the current theme (either light or dark). Initially, it's set to "light".
- `init_ui()`: A method that sets up the user interface (UI) of the application.

### 3. `init_ui` Method
```python
def init_ui(self):
    """
    Initializes the main user interface.
    Sets up the main window, text area, and menu bar.
    """
    self.setWindowTitle("Notebook")
    self.setGeometry(100, 100, 800, 600)
```
- Sets the window title as **"Notebook"**.
- The window is set to appear at position (100, 100) on the screen with a width of 800px and height of 600px.

### 4. Setting up the Text Area
```python
    self.text_area = QTextEdit(self)
    self.text_area.setFont(QFont("Arial", 14))
    self.setCentralWidget(self.text_area)
```
- `QTextEdit`: Creates a text area where users can input and edit text.
- The font for the text area is set to **Arial** with a font size of 14.
- `setCentralWidget(self.text_area)`: Makes the text area the central widget of the main window.

### 5. Applying the Theme (CSS)
```python
    self.apply_css("styles/light.css")
```
- `apply_css`: Applies a CSS file to style the application (set light theme by default).
  
### 6. Creating the Menu Bar
```python
    self.menu_bar = QMenuBar(self)
    self.setMenuBar(self.menu_bar)
    self.create_menus()
```
- `QMenuBar`: Creates a menu bar at the top of the window.
- `setMenuBar(self.menu_bar)`: Sets this menu bar to the main window.
- `create_menus()`: A method that will define and add menus and actions to the menu bar.

### 7. `create_menus` Method
```python
def create_menus(self):
    """
    Creates the menu bar and adds actions to the menus.
    """
```
- `create_menus`: This method defines all the menus (File, Edit, View, Font) and the actions for each.

### 8. File Menu Actions
```python
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
```
- `QAction`: Creates an action for each menu item with an associated icon and text.
- **Triggering actions**: Each action is connected to a method (like `new_file`, `open_file`, etc.) that performs a specific function when the action is triggered.
- **Adding actions to file menu**: These actions (New, Open, Save, etc.) are added to the "File" menu.

### 9. Edit, View, and Font Menus
```python
    edit_menu = self.menu_bar.addMenu("Edit")
    find_action = QAction("Find...", self)
    find_action.triggered.connect(self.find_text)
    edit_menu.addAction(find_action)

    view_menu = self.menu_bar.addMenu("View")
    toggle_theme_action = QAction("Toggle Theme", self)
    toggle_theme_action.triggered.connect(self.toggle_theme)
    view_menu.addAction(toggle_theme_action)

    font_menu = self.menu_bar.addMenu("Font")
    change_font_action = QAction("Change to Courier", self)
    change_font_action.triggered.connect(self.change_font)
    font_menu.addAction(change_font_action)
```
- **Edit Menu**: Contains a "Find" action to search for specific text in the document.
- **View Menu**: Allows toggling between light and dark themes.
- **Font Menu**: Provides an option to change the text font to "Courier".

### 10. `apply_css` Method
```python
def apply_css(self, css_file):
    """
    Applies a CSS file to the application.
    """
    try:
        with open(css_file, "r") as file:
            self.setStyleSheet(file.read())
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Could not load stylesheet:\n{e}")
```
- Reads a CSS file and applies it to the application using `setStyleSheet`.
- If the CSS file cannot be loaded, it displays an error message using `QMessageBox`.

### 11. File Actions Methods (New, Open, Save, Export)
- `new_file`: Clears the text area.
- `open_file`: Opens a file and loads its content into the text area.
- `save_file`: Saves the content of the text area to a file.
- `export_to_pdf`: Exports the content of the text area to a PDF file using `FPDF`.

### 12. Search and Change Font
- `find_text`: Searches for text in the document. Displays a dialog where the user can input the text to search.
- `change_font`: Changes the font of the text area to **Courier**.

### 13. Theme Toggle
```python
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
```
- Toggles the theme between light and dark by applying different CSS files (`light.css` or `dark.css`).

### 14. Running the Application
```python
if __name__ == "__main__":
    app = QApplication(sys.argv)
    notebook = Notebook()
    notebook.show()
    sys.exit(app.exec_())
```
- This block starts the application by creating an instance of `QApplication` and running the `Notebook` application window.
- The event loop is started with `app.exec_()`, keeping the window open and responsive until closed.

---

### Summary

- The app provides a basic text editor with file handling, search functionality, font changes, theme toggling, and PDF export.
- The GUI is structured with a menu bar allowing for intuitive navigation and user interaction.
