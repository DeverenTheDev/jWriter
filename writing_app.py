import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class WritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Writing App")
        self.scenes = {}  # Dictionary to store scenes and their content
        self.current_scene = None  # Tracks the currently selected scene

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
        file_menu.add_command(label="Exit", command=self.root.quit)
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

    def new_project(self):
        # Code to create a new project
        self.scenes.clear()
        self.tree.delete(*self.tree.get_children())
        self.text_editor.delete("1.0", tk.END)
        messagebox.showinfo("New Project", "Started a new project.")

    def open_project(self):
        # Placeholder for opening an existing project
        file_path = filedialog.askopenfilename(title="Open Project")
        if file_path:
            messagebox.showinfo("Open Project", f"Opened {file_path}")

    def save_project(self):
        # Placeholder for saving the current project
        file_path = filedialog.asksaveasfilename(title="Save Project")
        if file_path:
            messagebox.showinfo("Save Project", f"Saved to {file_path}")

    def add_scene(self):
        # Add a new scene
        scene_name = f"Scene {len(self.scenes) + 1}"
        self.scenes[scene_name] = ""  # Initialize scene content as empty
        self.tree.insert("", "end", iid=scene_name, text=scene_name)
        messagebox.showinfo("Add Scene", f"Added {scene_name}")

    def load_scene(self, event):
        # Load the selected scene's content into the text editor
        selected_item = self.tree.selection()
        if selected_item:
            scene_name = self.tree.item(selected_item, "text")
            self.current_scene = scene_name
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert("1.0", self.scenes.get(scene_name, ""))

    def save_current_scene(self):
        # Save the current scene's content from the text editor
        if self.current_scene:
            self.scenes[self.current_scene] = self.text_editor.get("1.0", tk.END).strip()


if __name__ == "__main__":
    root = tk.Tk()
    app = WritingApp(root)
    root.mainloop()
