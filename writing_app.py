import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

class WritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Writing App")
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
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(self.main_frame)
        self.tree.heading("#0", text="Scenes", anchor="w")
        self.tree.pack(fill="both", expand=True)

        self.add_button = ttk.Button(self.main_frame, text="Add Scene", command=self.add_scene)
        self.add_button.pack(pady=5)

    def new_project(self):
        # Code to create a new project
        messagebox.showinfo("New Project", "Create a new project")

    def open_project(self):
        # Code to open an existing project
        file_path = filedialog.askopenfilename(title="Open Project")
        if file_path:
            messagebox.showinfo("Open Project", f"Opened {file_path}")

    def save_project(self):
        # Code to save the project
        file_path = filedialog.asksaveasfilename(title="Save Project")
        if file_path:
            messagebox.showinfo("Save Project", f"Saved to {file_path}")

    def add_scene(self):
        # Add a new scene to the treeview
        self.tree.insert("", "end", text=f"Scene {len(self.tree.get_children()) + 1}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WritingApp(root)
    root.mainloop()
