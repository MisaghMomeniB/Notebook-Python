# 📝 Notebook Application

**Notebook** is a simple and practical application for note-taking, built using **PyQt**. This project allows you to manage your notes efficiently with a clean and straightforward interface.

---

## 🚀 Features

- User-friendly graphical interface  
- Manage and display notes effortlessly  
- Easily extendable and customizable  

---

## 🛠️ Prerequisites

To run this project, you need the following:

- Python 3.6 or later  
- PyQt5  

Install the required libraries using the following command:

```bash
pip install PyQt5
```

---

## 📦 Running the Application

To run the application, execute the following command:

```bash
python main.py
```

---

## 🧩 Code Analysis

### **Imports**
```python
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QMenuBar, QAction, QFileDialog, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont, QIcon
from fpdf import FPDF
```

1. **`import sys`**:  
   - Provides access to system-specific parameters and functions, such as command-line arguments (`sys.argv`).

2. **`from PyQt5.QtWidgets import ...`**:  
   - Imports key PyQt5 widgets used for building the GUI, including:
     - **`QApplication`**: The core application class for PyQt5 programs.  
     - **`QMainWindow`**: A main application window with standard features like toolbars and menus.  
     - **`QTextEdit`**: A widget for multiline text editing.  
     - **`QMenuBar`**: A menu bar widget for adding menus.  
     - **`QAction`**: Represents actions such as buttons in menus.  
     - **`QFileDialog`**: For file open/save dialog boxes.  
     - **`QMessageBox`**: For pop-up message dialogs.  
     - **`QInputDialog`**: For simple input dialogs.

3. **`from PyQt5.QtGui import QFont, QIcon`**:  
   - **`QFont`**: Used for setting font properties.  
   - **`QIcon`**: Represents icons for buttons, menus, or windows.

4. **`from fpdf import FPDF`**:  
   - Imports the `FPDF` class for generating PDF files programmatically.

---

### **Defining the Notebook Class**
```python
class Notebook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"  # Current theme, default is light
        self.init_ui()
```

5. **`class Notebook(QMainWindow):`**:  
   - Defines the `Notebook` class, which inherits from `QMainWindow` to create a GUI application with standard window features.

6. **`def __init__(self):`**:  
   - Initializes the class.  

7. **`super().__init__()`**:  
   - Calls the parent class (`QMainWindow`) constructor to ensure proper initialization.

8. **`self.current_theme = "light"`**:  
   - A class attribute to store the current theme (`light` or `dark`).

9. **`self.init_ui()`**:  
   - Calls the `init_ui` method to set up the user interface.

---

### **Setting Up the UI**
```python
def init_ui(self):
    self.setWindowTitle("Notebook")
    self.setGeometry(100, 100, 800, 600)
    self.text_area = QTextEdit(self)
    self.text_area.setFont(QFont("Arial", 14))
    self.setCentralWidget(self.text_area)
    self.apply_css("styles/light.css")
    self.menu_bar = QMenuBar(self)
    self.setMenuBar(self.menu_bar)
    self.create_menus()
```

10. **`self.setWindowTitle("Notebook")`**:  
    - Sets the window title to "Notebook".

11. **`self.setGeometry(100, 100, 800, 600)`**:  
    - Positions the window at `(100, 100)` on the screen with a width of `800` and height of `600`.

12. **`self.text_area = QTextEdit(self)`**:  
    - Creates a text editing widget as the main area for typing notes.

13. **`self.text_area.setFont(QFont("Arial", 14))`**:  
    - Sets the font of the text area to Arial with a size of 14.

14. **`self.setCentralWidget(self.text_area)`**:  
    - Makes the text area the central widget of the main window.

15. **`self.apply_css("styles/light.css")`**:  
    - Applies a light theme by loading a CSS file.

16. **`self.menu_bar = QMenuBar(self)`**:  
    - Creates a menu bar for adding menus and actions.

17. **`self.setMenuBar(self.menu_bar)`**:  
    - Sets the created menu bar as the window's menu bar.

18. **`self.create_menus()`**:  
    - Calls the `create_menus` method to populate the menu bar.

---

### **Creating Menus**
```python
def create_menus(self):
    file_menu = self.menu_bar.addMenu("File")
    new_action = QAction(QIcon("icons/new.png"), "New", self)
    new_action.triggered.connect(self.new_file)
    ...
```

19. **`file_menu = self.menu_bar.addMenu("File")`**:  
    - Adds a "File" menu to the menu bar.

20. **`new_action = QAction(QIcon("icons/new.png"), "New", self)`**:  
    - Creates a "New" action with an icon.

21. **`new_action.triggered.connect(self.new_file)`**:  
    - Connects the "New" action to the `new_file` method, executed when the action is triggered.

*(Similar steps are repeated for other menus and actions, such as "Open", "Save", "Export to PDF", etc.)*

---

### **Methods for Menu Actions**
Each action method implements specific functionality:

- **`apply_css`**: Loads and applies a CSS theme.  
- **`new_file`**: Clears the text area.  
- **`open_file`**: Opens and loads text files into the text area.  
- **`save_file`**: Saves the text area's content to a file.  
- **`export_to_pdf`**: Converts text to a PDF using `FPDF`.  
- **`find_text`**: Searches for text in the editor.  
- **`change_font`**: Changes the text area font to Courier.  
- **`toggle_theme`**: Toggles between light and dark themes.

---

### **Main Program Execution**
```python
if __name__ == "__main__":
    app = QApplication(sys.argv)
    notebook = Notebook()
    notebook.show()
    sys.exit(app.exec_())
```

22. **`if __name__ == "__main__":`**:  
    - Ensures this block runs only when the script is executed directly.

23. **`app = QApplication(sys.argv)`**:  
    - Creates a PyQt application instance to manage GUI events.

24. **`notebook = Notebook()`**:  
    - Instantiates the `Notebook` application.

25. **`notebook.show()`**:  
    - Displays the main window.

26. **`sys.exit(app.exec_())`**:  
    - Starts the event loop and exits cleanly when the application is closed.

---
