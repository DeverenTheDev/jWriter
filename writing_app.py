import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import sqlite3


class WritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Writing App")
        self.root.geometry("800x600")

        # Database variables
        self.conn = None
        self.current_scene = None

        # Create GUI elements
        self.create_menu()
        self.create_toolbar()
        self.create_main_window()
        self.create_status_bar()

    def create_menu(self):
        """Create the top menu bar."""
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # File Menu
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Open Project", command=self.open_project)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.close_app)
        menu.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(menu, tearoff=False)
        edit_menu.add_command(label="Undo", command=lambda: self.text_editor.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", command=lambda: self.text_editor.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_editor.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_editor.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_editor.event_generate("<<Paste>>"))
        menu.add_cascade(label="Edit", menu=edit_menu)

        # View Menu (Placeholder for future functionality)
        view_menu = tk.Menu(menu, tearoff=False)
        view_menu.add_command(label="Zoom In", command=lambda: messagebox.showinfo("Zoom", "Zoom In feature coming soon!"))
        view_menu.add_command(label="Zoom Out", command=lambda: messagebox.showinfo("Zoom", "Zoom Out feature coming soon!"))
        menu.add_cascade(label="View", menu=view_menu)

    def create_toolbar(self):
        """Create a toolbar with formatting options."""
        toolbar = ttk.Frame(self.root, padding=5)
        toolbar.pack(side="top", fill="x")

        # Bold Button
        bold_btn = ttk.Button(toolbar, text="Bold", command=self.toggle_bold)
        bold_btn.pack(side="left", padx=2)

        # Italic Button
        italic_btn = ttk.Button(toolbar, text="Italic", command=self.toggle_italic)
        italic_btn.pack(side="left", padx=2)

        # Font Size Dropdown
        font_sizes = [10, 12, 14, 16, 18, 20, 24]
        self.font_size_var = tk.IntVar(value=12)
        font_size_menu = ttk.Combobox(toolbar, textvariable=self.font_size_var, values=font_sizes, width=5)
        font_size_menu.bind("<<ComboboxSelected>>", self.change_font_size)
        font_size_menu.pack(side="left", padx=5)

    def create_main_window(self):
        """Create the main window layout."""
        self.main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_frame.pack(fill="both", expand=True)

        # Left panel: Scene list
        self.scene_frame = ttk.Frame(self.main_frame, width=200)
        self.main_frame.add(self.scene_frame, weight=1)

        self.tree = ttk.Treeview(self.scene_frame)
        self.tree.heading("#0", text="Scenes", anchor="w")
        self.tree.bind("<<TreeviewSelect>>", self.load_scene)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.add_button = ttk.Button(self.scene_frame, text="Add Scene", command=self.add_scene)
        self.add_button.pack(pady=5)

        # Right panel: Text editor
        self.editor_frame = ttk.Frame(self.main_frame)
        self.main_frame.add(self.editor_frame, weight=3)

        self.text_editor = tk.Text(self.editor_frame, wrap="word", undo=True, font=("Arial", 12))
        self.text_editor.pack(fill="both", expand=True, padx=5, pady=5)

    def create_status_bar(self):
        """Create a status bar at the bottom."""
        self.status_bar = ttk.Label(self.root, text="Ready", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

    def update_status_bar(self, message):
        """Update the status bar with a custom message."""
        self.status_bar.config(text=message)

    def toggle_bold(self):
        """Toggle bold formatting."""
        current_tags = self.text_editor.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_editor.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.text_editor.tag_add("bold", "sel.first", "sel.last")
            bold_font = font.Font(self.text_editor, self.text_editor.cget("font"))
            bold_font.configure(weight="bold")
            self.text_editor.tag_configure("bold", font=bold_font)

    def toggle_italic(self):
        """Toggle italic formatting."""
        current_tags = self.text_editor.tag_names("sel.first")
        if "italic" in current_tags:
            self.text_editor.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.text_editor.tag_add("italic", "sel.first", "sel.last")
            italic_font = font.Font(self.text_editor, self.text_editor.cget("font"))
            italic_font.configure(slant="italic")
            self.text_editor.tag_configure("italic", font=italic_font)

    def change_font_size(self, event):
        """Change the font size of the text editor."""
        new_size = self.font_size_var.get()
        current_font = font.Font(self.text_editor, self.text_editor.cget("font"))
        current_font.configure(size=new_size)
        self.text_editor.config(font=current_font)

    # Database and scene management methods (from previous code)

    def add_scene(self):
        """Add a new scene."""
        pass  # Same logic as before

    def load_scene(self, event):
        """Load scene into editor."""
        pass  # Same logic as before

    def save_project(self):
        """Save project data."""
        pass  # Same logic as before

    def new_project(self):
        """Create a new project."""
        pass  # Same logic as before

    def open_project(self):
        """Open an existing project."""
        pass  # Same logic as before

    def close_app(self):
        """Close the application."""
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = WritingApp(root)
    root.mainloop()
