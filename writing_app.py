import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class WritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Writing App")

        # Database connection variables
        self.conn = None  # SQLite connection
        self.current_scene = None  # Currently selected scene

        self.create_menu()
        self.create_main_window()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Open Project", command=self.open_project)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.close_app)
        menu.add_cascade(label="File", menu=file_menu)

    def create_main_window(self):
        # Split the main window into two sections: scene list and text editor
        self.main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_frame.pack(fill="both", expand=True)

        # Left panel: Scene List
        self.scene_frame = ttk.Frame(self.main_frame, width=200)
        self.main_frame.add(self.scene_frame, weight=1)

        self.tree = ttk.Treeview(self.scene_frame)
        self.tree.heading("#0", text="Scenes", anchor="w")
        self.tree.bind("<<TreeviewSelect>>", self.load_scene)  # Load scene on selection
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.add_button = ttk.Button(self.scene_frame, text="Add Scene", command=self.add_scene)
        self.add_button.pack(pady=5)

        # Right panel: Text Editor
        self.editor_frame = ttk.Frame(self.main_frame)
        self.main_frame.add(self.editor_frame, weight=3)

        self.text_editor = tk.Text(self.editor_frame, wrap="word")
        self.text_editor.pack(fill="both", expand=True, padx=5, pady=5)

    def connect_to_database(self, db_path):
        """Connect to SQLite database and set up tables."""
        self.conn = sqlite3.connect(db_path)
        cursor = self.conn.cursor()

        # Create the scenes table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scenes (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                content TEXT
            )
        """)
        self.conn.commit()

    def new_project(self):
        """Create a new project and database."""
        file_path = filedialog.asksaveasfilename(
            title="New Project",
            defaultextension=".db",
            filetypes=[("Database Files", "*.db")]
        )
        if file_path:
            self.connect_to_database(file_path)
            self.tree.delete(*self.tree.get_children())
            self.text_editor.delete("1.0", tk.END)
            messagebox.showinfo("New Project", "Started a new project.")

    def open_project(self):
        """Open an existing project database."""
        file_path = filedialog.askopenfilename(
            title="Open Project",
            filetypes=[("Database Files", "*.db")]
        )
        if file_path:
            self.connect_to_database(file_path)
            self.load_scenes()
            messagebox.showinfo("Open Project", f"Opened {file_path}")

    def save_project(self):
        """Save changes to the current project."""
        if self.current_scene:
            self.save_current_scene()
            messagebox.showinfo("Save Project", "Project saved successfully.")

    def add_scene(self):
        """Add a new scene to the database and display it."""
        scene_name = f"Scene {len(self.tree.get_children()) + 1}"
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO scenes (name, content) VALUES (?, ?)", (scene_name, ""))
            self.conn.commit()
            self.tree.insert("", "end", iid=scene_name, text=scene_name)
            messagebox.showinfo("Add Scene", f"Added {scene_name}")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Scene name already exists.")

    def load_scenes(self):
        """Load all scenes from the database into the treeview."""
        self.tree.delete(*self.tree.get_children())  # Clear the treeview
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM scenes")
        for (scene_name,) in cursor.fetchall():
            self.tree.insert("", "end", iid=scene_name, text=scene_name)

    def load_scene(self, event):
        """Load the selected scene's content into the text editor."""
        selected_item = self.tree.selection()
        if selected_item:
            scene_name = self.tree.item(selected_item, "text")
            self.current_scene = scene_name
            cursor = self.conn.cursor()
            cursor.execute("SELECT content FROM scenes WHERE name = ?", (scene_name,))
            result = cursor.fetchone()
            if result:
                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert("1.0", result[0])

    def save_current_scene(self):
        """Save the current scene's content into the database."""
        if self.current_scene:
            content = self.text_editor.get("1.0", tk.END).strip()
            cursor = self.conn.cursor()
            cursor.execute("UPDATE scenes SET content = ? WHERE name = ?", (content, self.current_scene))
            self.conn.commit()

    def close_app(self):
        """Close the application and clean up."""
        if self.conn:
            self.conn.close()
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = WritingApp(root)
    root.mainloop()
