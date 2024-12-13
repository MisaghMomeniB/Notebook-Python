# 📝 **Notebook Application**

This is a **Notebook** application built with **PyQt5**, which allows users to create, edit, save, open, and export text files. The app also supports exporting text to PDFs, searching for text, changing font styles, and toggling between light and dark themes.

### 🚀 **Features:**
- **Create, Open, Save, and Export Files**: Manage text files with support for text file format and PDF export.
- **Find and Highlight Text**: Search and highlight specific text in your document.
- **Change Font**: Switch between different fonts, such as Courier.
- **Toggle Themes**: Switch between light and dark themes for comfortable reading and editing.
- **Intuitive User Interface**: A clean, user-friendly interface built with PyQt5, complete with a menu bar for easy navigation.

---

### 🧑‍💻 **Getting Started:**

To run the notebook application, you need to have Python installed along with the necessary dependencies.

#### 📥 **Prerequisites:**
1. **Python 3.x** (or later) installed on your system.
2. Install the required libraries using `pip`:
    ```bash
    pip install pyqt5 fpdf
    ```

#### 📂 **How to Run:**
1. **Download** the repository or script to your local machine.
2. **Update the File Paths** (if necessary):
    - Ensure that you have `icons/` and `styles/` folders containing the appropriate files (e.g., `new.png`, `open.png`, `light.css`, `dark.css`).
3. **Run the Application**:
    ```bash
    python notebook.py
    ```

---

### 🔧 **Code Breakdown:**

#### 1. **Main Window**:
   The main window contains a text area where users can write, edit, and format their text. It also features a menu bar for managing files and editing the text.

```python
self.text_area = QTextEdit(self)
self.text_area.setFont(QFont("Arial", 14))
```

#### 2. **Menu Bar**:
   The menu bar provides options to manage files, change fonts, toggle themes, and search text. It includes the following menus:
   - **File**: New, Open, Save, Export to PDF, Exit
   - **Edit**: Find
   - **View**: Toggle Theme (Light/Dark)
   - **Font**: Change to Courier

```python
file_menu = self.menu_bar.addMenu("File")
view_menu = self.menu_bar.addMenu("View")
```

#### 3. **File Management**:
   - **New File**: Clears the text area for a new document.
   - **Open File**: Allows the user to open a text file and display its content.
   - **Save File**: Saves the current content of the text area to a file.
   - **Export to PDF**: Exports the content to a PDF file.

```python
new_action.triggered.connect(self.new_file)
open_action.triggered.connect(self.open_file)
save_action.triggered.connect(self.save_file)
```

#### 4. **Text Search**:
   The app allows users to search for specific text in the document, making it easy to find specific information.

```python
search_text, ok = QInputDialog.getText(self, "Find Text", "Enter text to search:")
```

#### 5. **Font and Theme Customization**:
   - **Change Font**: Users can switch to a fixed-width font (Courier) for easier reading and writing.
   - **Toggle Theme**: Switch between light and dark themes for optimal user experience.

```python
self.text_area.setFont(QFont("Courier", 14))
self.apply_css("styles/dark.css")
```

---

### 🎨 **User Interface:**

The application features an intuitive interface with the following:
- **Text Area**: Where users can enter and edit text.
- **Menu Bar**: For file management, editing, and customization options.
- **Themes**: Switch between light and dark modes to reduce eye strain.

---

### ⚙️ **Additional Features:**
- **Text Formatting**: While this basic version does not support rich text formatting, future versions could implement this feature.
- **Export Options**: You can save your notes in `.txt` format or export them as a `.pdf` document.
- **Search Functionality**: Helps quickly find specific words or phrases in the text area.

---

### 🔄 **Future Improvements**:
- **Support for Rich Text Formatting**: Add options for bold, italic, underline, and more.
- **Additional Themes**: Include more theme options (e.g., custom user themes).
- **Cloud Sync**: Allow syncing documents across devices.

---

### 💬 **Feedback & Contributions:**
We welcome feedback, suggestions, and contributions! Feel free to fork the repository, submit issues, or create pull requests to improve the application.

---

### 🙏 **Thank You!**
Thank you for exploring the **Notebook Application**! We hope it helps you stay organized and productive while writing and editing your notes. Enjoy using the app, and happy writing! 📝
