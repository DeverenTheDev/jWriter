import json  # For saving and loading project data


def new_project(self):
    """Create a new project."""
    if messagebox.askyesno("New Project", "Are you sure you want to create a new project? Unsaved changes will be lost."):
        self.text_editor.delete("1.0", tk.END)  # Clear the text editor
        for item in self.tree.get_children():
            self.tree.delete(item)  # Clear the scene list
        self.current_scene = None
        self.update_status_bar("New project created.")


def open_project(self):
    """Open an existing project."""
    file_path = filedialog.askopenfilename(
        title="Open Project",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "r") as file:
                project_data = json.load(file)
                # Load scenes into the treeview
                self.tree.delete(*self.tree.get_children())
                for scene in project_data.get("scenes", []):
                    self.tree.insert("", "end", text=scene)
                # Load text into the editor
                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert("1.0", project_data.get("content", ""))
                self.update_status_bar(f"Opened project: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open project: {e}")


def save_project(self):
    """Save project data."""
    file_path = filedialog.asksaveasfilename(
        title="Save Project",
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            # Collect data to save
            scenes = [self.tree.item(child)["text"] for child in self.tree.get_children()]
            content = self.text_editor.get("1.0", tk.END).strip()
            project_data = {
                "scenes": scenes,
                "content": content,
            }
            # Write to file
            with open(file_path, "w") as file:
                json.dump(project_data, file, indent=4)
            self.update_status_bar(f"Project saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save project: {e}")
