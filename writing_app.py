import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import sqlite3
import os


class WritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Writing App")
        self.root.geometry("800x600")

        # Database variables
        self.conn = None
        self.current_project_path = None

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

    def create_toolbar(self):
        """Create a toolbar with formatting options."""
        toolbar = ttk.Frame(self.root, padding=5)
        toolbar.pack(side="top", fill="x")

        bold_btn = ttk.Button(toolbar, text="Bold", command=self.toggle_bold)
        bold_btn.pack(side="left", padx=2)

        italic_btn = ttk.Button(toolbar, text="Italic", command=self.toggle_italic)
        italic_btn.pack(side="left", padx=2)

        font_sizes = [10, 12, 14, 16, 18, 20, 24]
        self.font_size_var = tk.IntVar(value=12)
        font_size_menu = ttk.Combobox(toolbar, textvariable=self.font_size_var, values=font_sizes, width=5)
        font_size_menu.bind("<<ComboboxSelected>>", self.change_font_size)
        font_size_menu.pack(side="left", padx=5)

    def create_main_window(self):
        """Create the main window layout."""
        self.main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_frame.pack(fill="both", expand=True)

        # Left panel: Scenes
        self.scene_frame = ttk.Frame(self.main_frame, width=200)
        self.main_frame.add(self.scene_frame, weight=1)

        self.tree = ttk.Treeview(self.scene_frame)
        self.tree.heading("#0", text="Scenes", anchor="w")
        self.tree.bind("<<TreeviewSelect>>", self.load_scene)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.add_button = ttk.Button(self.scene_frame, text="Add Scene", command=self.add_scene)
        self.add_button.pack(pady=5)

        # Middle panel: Text editor
        self.editor_frame = ttk.Frame(self.main_frame)
        self.main_frame.add(self.editor_frame, weight=3)

        self.text_editor = tk.Text(self.editor_frame, wrap="word", undo=True, font=("Arial", 12))
        self.text_editor.pack(fill="both", expand=True, padx=5, pady=5)

        # Right panel: Notes
        self.notes_frame = ttk.Frame(self.main_frame, width=200)
        self.main_frame.add(self.notes_frame, weight=1)

        self.notes_tree = ttk.Treeview(self.notes_frame)
        self.notes_tree.heading("#0", text="Notes", anchor="w")
        self.notes_tree.bind("<<TreeviewSelect>>", self.load_note)  # Define load_note method
        self.notes_tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.add_note_button = ttk.Button(self.notes_frame, text="Add Note", command=self.add_note)
        self.add_note_button.pack(pady=5)


    def add_note(self):
        """Add a new note."""
        note_name = f"Note {len(self.notes_tree.get_children()) + 1}"
        self.notes_tree.insert("", "end", text=note_name)
        self.update_status_bar(f"Added {note_name}")

    def load_note(self, event):
        """Load the selected note into the editor."""
        selected_item = self.notes_tree.focus()
        if selected_item:
            note_name = self.notes_tree.item(selected_item, "text")
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert("1.0", f"Content for {note_name}")
            self.update_status_bar(f"Loaded {note_name}")



    def create_status_bar(self):
        """Create a status bar at the bottom."""
        self.status_bar = ttk.Label(self.root, text="Ready", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

    def update_status_bar(self, message):
        """Update the status bar with a custom message."""
        self.status_bar.config(text=message)

    def new_project(self):
        """Create a new project."""
        if self.conn:
            self.conn.close()
        self.text_editor.delete("1.0", tk.END)
        self.tree.delete(*self.tree.get_children())
        self.current_project_path = None
        self.conn = None
        self.update_status_bar("New project created.")

    def open_project(self):
        """Open an existing project."""
        project_path = filedialog.askopenfilename(
            title="Open Project",
            filetypes=(("SQLite Database Files", "*.db"), ("All Files", "*.*"))
        )
        if project_path:
            self.current_project_path = project_path
            if self.conn:
                self.conn.close()
            self.conn = sqlite3.connect(self.current_project_path)
            self.load_scenes_from_db()
            self.update_status_bar(f"Opened project: {os.path.basename(project_path)}")

    def save_project(self):
        """Save the current project."""
        if not self.current_project_path:
            project_path = filedialog.asksaveasfilename(
                title="Save Project",
                defaultextension=".db",
                filetypes=(("SQLite Database Files", "*.db"), ("All Files", "*.*"))
            )
            if not project_path:
                return
            self.current_project_path = project_path
            self.conn = sqlite3.connect(self.current_project_path)
            self.create_db_schema()

        self.save_scenes_to_db()
        self.update_status_bar(f"Project saved: {os.path.basename(self.current_project_path)}")

    def create_db_schema(self):
        """Create the database schema."""
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS scenes (id INTEGER PRIMARY KEY, name TEXT, content TEXT)")
        self.conn.commit()

    def save_scenes_to_db(self):
        """Save scenes to the database."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM scenes")
        for item in self.tree.get_children():
            scene_name = self.tree.item(item, "text")
            scene_content = self.text_editor.get("1.0", tk.END).strip() if item == self.current_scene else ""
            cursor.execute("INSERT INTO scenes (name, content) VALUES (?, ?)", (scene_name, scene_content))
        self.conn.commit()

    def load_scenes_from_db(self):
        """Load scenes from the database."""
        self.tree.delete(*self.tree.get_children())
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM scenes")
        for row in cursor.fetchall():
            self.tree.insert("", "end", text=row[1], iid=row[0])
        self.update_status_bar("Scenes loaded.")

    def add_scene(self):
        """Add a new scene."""
        scene_name = f"Scene {len(self.tree.get_children()) + 1}"
        self.tree.insert("", "end", text=scene_name)
        self.update_status_bar(f"Added {scene_name}")

    def load_scene(self, event):
        """Load the selected scene into the editor."""
        selected_item = self.tree.focus()
        if selected_item:
            cursor = self.conn.cursor()
            cursor.execute("SELECT content FROM scenes WHERE id=?", (selected_item,))
            row = cursor.fetchone()
            if row:
                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert("1.0", row[0])
                self.current_scene = selected_item
                self.update_status_bar(f"Loaded {self.tree.item(selected_item, 'text')}")

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

    def close_app(self):
        """Close the application."""
        if self.conn:
            self.conn.close()
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = WritingApp(root)
    root.mainloop()
