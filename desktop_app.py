import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
from tkmacosx import Button

# File paths for storage
TASKS_FILE = "tasks.json"
USERS_FILE = "users.json"

# Load data from files
def load_data(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save data to files
def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Main App Class
class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management App")
        self.root.geometry("800x500")
        self.user = None  # Logged-in user

        # Initialize data
        self.users = load_data(USERS_FILE)
        self.tasks = load_data(TASKS_FILE)

        # Styling
        self.bg_color = "#f5f5f5"
        self.button_color = "#2196F3"
        self.button_color_green = "#08c982"
        self.text_color = "#ffffff"

        self.root.configure(bg=self.bg_color)

        # Show login screen
        self.show_login_screen()

    def show_login_screen(self):
        """Display login screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        
        # Add a label with the title
        tk.Label(self.root, text="Welcome to Task Manager", font=("Helvetica", 24)).pack(pady=20)  # Add padding for spacing

        tk.Label(self.root, text="Username:", bg=self.bg_color).pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", bg=self.bg_color).pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        Button(
                    self.root,
                    font=("Arial", 12),
                    text="Login",
                    bg=self.button_color_green,
                    fg=self.text_color,
                    command=lambda: self.login(username_entry.get(), password_entry.get()),
                    borderless=1
                ).pack(pady=10)

       
        Button(
            self.root,
            text="Register",
            bg=self.button_color,
            fg=self.text_color,
            borderless=1 ,
            font=("Arial", 12),
            command=self.show_registration_screen
        ).pack(pady=10)

    def login(self, username, password):
        """Authenticate user."""
        if username in self.users and self.users[username] == password:
            self.user = username
            self.show_task_list_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def show_registration_screen(self):
        """Display registration screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Username:", bg=self.bg_color).pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", bg=self.bg_color).pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)
    
        Button(
            self.root,
            text="Register",
            bg=self.button_color,
            fg=self.text_color,
            borderless=1 ,
            font=("Arial", 12),
            command=lambda: self.register(username_entry.get(), password_entry.get()),
        ).pack(pady=10)

    def register(self, username, password):
        """Register a new user."""
        if username in self.users:
            messagebox.showerror("Error", "Username already exists.")
            return
        if not username or not password:
            messagebox.showerror("Error", "Both fields are required.")
            return

        self.users[username] = password
        save_data(USERS_FILE, self.users)
        messagebox.showinfo("Success", "Registration successful! You can now log in.")
        self.show_login_screen()

    def show_task_list_screen(self):
        """Display task list screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root, text=f"Logged in as: {self.user}", bg=self.bg_color, font=("Arial", 12, "bold")
        ).pack(pady=5)

        Button(
            self.root, text="Add New Task", bg=self.button_color_green,  fg=self.text_color,
            borderless=1 ,
            font=("Arial", 12), command=self.show_add_task_screen
        ).pack(pady=10)

        Button(
            self.root, text="Filter Tasks", bg=self.button_color,  fg=self.text_color,
            borderless=1 ,
            font=("Arial", 12), command=self.filter_tasks
        ).pack(pady=10)

        self.task_tree = ttk.Treeview(
            self.root, columns=("Name", "Priority", "Due Date", "Timestamp", "Completed"), show="headings"
        )
        self.task_tree.heading("Name", text="Name")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Due Date", text="Due Date")
        self.task_tree.heading("Timestamp", text="Timestamp")
        self.task_tree.heading("Completed", text="Completed")
        self.task_tree.pack(fill="both", expand=True)

        self.task_tree.bind("<Double-1>", self.edit_task)  # Double-click to edit
        Button(
            self.root, text="Delete Task", bg=self.button_color,  fg=self.text_color,
            borderless=1 ,
            font=("Arial", 12), command=self.confirm_delete
        ).pack(pady=10)

        self.refresh_task_list()

    def confirm_delete(self):
        """Show confirmation dialog before deletion."""
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this task?")
        if response:  # If the user clicked 'Yes'
            self.delete_task()
        else:  # If the user clicked 'No'
            print("Task not deleted")


    def show_add_task_screen(self, task=None):
        """Display add/edit task screen."""
        add_task_window = tk.Toplevel(self.root)
        add_task_window.title("Add/Edit Task")
        add_task_window.geometry("400x500")
        add_task_window.configure(bg=self.bg_color)

        tk.Label(add_task_window, text="Task Name:", bg=self.bg_color).pack(pady=5)
        name_entry = tk.Entry(add_task_window)
        name_entry.pack(pady=5)

        tk.Label(add_task_window, text="Priority:", bg=self.bg_color).pack(pady=5)
        priority_combo = ttk.Combobox(add_task_window, values=["High", "Medium", "Low"], state="readonly")
        priority_combo.pack(pady=5)

        tk.Label(add_task_window, text="Due Date (YYYY-MM-DD):", bg=self.bg_color).pack(pady=5)
        due_date_entry = tk.Entry(add_task_window)
        due_date_entry.pack(pady=5)

        tk.Label(add_task_window, text="Description:", bg=self.bg_color).pack(pady=5)
        description_text = tk.Text(add_task_window, height=5, width=40)
        description_text.pack(pady=5)

        if task:
            name_entry.insert(0, task["name"])
            priority_combo.set(task["priority"])
            due_date_entry.insert(0, task["due_date"])
            description_text.insert("1.0", task["description"])

        Button(
            add_task_window,
            text="Save",
            bg=self.button_color,
             fg=self.text_color,
            borderless=1 ,
            font=("Arial", 12),
            command=lambda: self.save_task(
                name_entry.get(),
                priority_combo.get(),
                due_date_entry.get(),
                description_text.get("1.0", "end").strip(),
                add_task_window,
                task,
            ),
        ).pack(pady=10)

    def save_task(self, name, priority, due_date, description, window, task=None):
        """Save a new or updated task."""
        if not name or not priority or not due_date or not description:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
            if due_date_obj < datetime.now():
                messagebox.showerror("Error", "Due date cannot be in the past.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid date format.")
            return

        if self.user not in self.tasks:
            self.tasks[self.user] = []

        if task:
            self.tasks[self.user].remove(task)

        self.tasks[self.user].append(
            {
                "name": name,
                "priority": priority,
                "due_date": due_date,
                "description": description,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "completed": False,  # New task is not completed by default
            }
        )

        save_data(TASKS_FILE, self.tasks)
        self.refresh_task_list()
        window.destroy()

    def refresh_task_list(self):
        """Refresh the task list display."""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        if self.user in self.tasks:
            for task in self.tasks[self.user]:
                self.task_tree.insert(
                    "", "end", values=(task["name"], task["priority"], task["due_date"], task["timestamp"], "✔" if task["completed"] else "❌")
                )

    def delete_task(self):
        """Delete the selected task."""
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected.")
            return

        task_values = self.task_tree.item(selected_item)["values"]
        
        task_found = False
        # Loop through tasks to find the matching task
        for task in self.tasks[self.user]:
            
            # Create a task tuple excluding the 'completed' field for comparison
            task_tuple = (task["name"], task["priority"], task["due_date"], task["timestamp"])
            
            # Compare the task tuple from list with the task values from the tree (ignoring 'completed')
            if task_tuple == tuple(task_values[:4]):  # Compare without 'completed' field
                self.tasks[self.user].remove(task)  # Remove the task
                task_found = True
                break
        
        if task_found:
            save_data(TASKS_FILE, self.tasks)
            self.refresh_task_list()
        else:
            messagebox.showerror("Error", "Task not found.")


    def get_task_index_by_id(self, selected_item):
        for idx, task in enumerate(self.tasks[self.user]):
            if task["timestamp"] == selected_item:  # or any unique identifier
                return idx
        return None


    def edit_task(self, event=None):
        """Allow the user to edit a selected task."""
        selected_item = self.task_tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a task to edit.")
            return

        # Get the selected task's current values
        task_data = self.task_tree.item(selected_item, "values")

        # Check if data is valid
        if len(task_data) < 5:
            messagebox.showerror("Error", "Invalid task data.")
            return

        task_name, priority, due_date, timestamp, completion_status = task_data

        # Create an edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("300x400")
        edit_window.configure(bg=self.bg_color)

        # Task Name
        tk.Label(edit_window, text="Task Name:", bg=self.bg_color).pack(pady=5)
        task_name_entry = tk.Entry(edit_window)
        task_name_entry.insert(0, task_name)
        task_name_entry.pack(pady=5)

        # Priority
        tk.Label(edit_window, text="Priority:", bg=self.bg_color).pack(pady=5)
        priority_combo = ttk.Combobox(edit_window, values=["High", "Medium", "Low"], state="readonly")
        priority_combo.set(priority)
        priority_combo.pack(pady=5)

        # Due Date
        tk.Label(edit_window, text="Due Date (YYYY-MM-DD):", bg=self.bg_color).pack(pady=5)
        due_date_entry = tk.Entry(edit_window)
        due_date_entry.insert(0, due_date)
        due_date_entry.pack(pady=5)

        # Completion Status (Checkbox or combobox)
        tk.Label(edit_window, text="Completion Status:", bg=self.bg_color).pack(pady=5)
        completion_status_combo = ttk.Combobox(edit_window, values=["Completed", "Pending"], state="readonly")
        completion_status_combo.set("Completed" if completion_status == "✔" else "Pending")
        completion_status_combo.pack(pady=5)

        # Save Button
        Button(
            edit_window,
            text="Save Changes",
            bg=self.button_color,
             fg=self.text_color,
            borderless=1 ,
            font=("Arial", 12),
            command=lambda: self.save_task_changes(
                selected_item, task_name_entry.get(), priority_combo.get(), due_date_entry.get(), completion_status_combo.get(), edit_window
            ),
        ).pack(pady=20)

    def save_task_changes(self, selected_item, task_name, priority, due_date, completion_status, edit_window):
        """Save the changes made to the selected task."""
        try:
            # Validate the inputs
            if not task_name or not due_date:
                messagebox.showerror("Error", "Task Name and Due Date are required.")
                return
            
            current_timestamp = self.task_tree.item(selected_item)["values"][3]
            # Update the task data
            updated_data = (
                task_name,
                priority,
                due_date,
                current_timestamp,  # You can keep the timestamp as is or update it
                "✔" if completion_status == "Completed" else "❌",
            )

            # Update the task in the tree view
            self.task_tree.item(selected_item, values=updated_data)

            # Optionally update the tasks list if you store tasks outside of the tree view
            task_index = self.get_task_index_by_id(selected_item)  # Modify if necessary to match your data structure
            if task_index is not None:
                self.tasks[self.user][task_index] = {
                    "name": task_name,
                    "priority": priority,
                    "due_date": due_date,
                    "timestamp": current_timestamp,  # Update with the actual timestamp if needed
                    "completed": completion_status == "Completed",
                }

            # Close the edit window
            edit_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving changes: {e}")


        """Edit the selected task."""
        selected_item = self.task_tree.selection()
        if not selected_item:
            return

        task_values = self.task_tree.item(selected_item)["values"]
        for task in self.tasks[self.user]:
            if (task["name"], task["priority"], task["due_date"], task["timestamp"]) == tuple(task_values):
                self.show_add_task_screen(task)
                break

    def filter_tasks(self):
        """Filter tasks based on priority or completion status."""
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Filter Tasks")
        filter_window.geometry("300x300")
        filter_window.configure(bg=self.bg_color)

        tk.Label(filter_window, text="Filter By:", bg=self.bg_color).pack(pady=10)

        # Option to filter by priority
        priority_label = tk.Label(filter_window, text="Priority:", bg=self.bg_color)
        priority_label.pack(pady=5)

        priority_combo = ttk.Combobox(filter_window, values=["All", "High", "Medium", "Low"], state="readonly")
        priority_combo.set("All")
        priority_combo.pack(pady=5)

        # Option to filter by completion status
        completed_label = tk.Label(filter_window, text="Completion Status:", bg=self.bg_color)
        completed_label.pack(pady=5)

        completed_combo = ttk.Combobox(filter_window, values=["All", "Completed", "Pending"], state="readonly")
        completed_combo.set("All")
        completed_combo.pack(pady=5)

        # Apply filter button
        Button(
            filter_window,
            text="Apply Filter",
            bg=self.button_color,
            fg=self.text_color,
            borderless=1 ,
            font=("Arial", 12),
            command=lambda: self.apply_filter(
                priority_combo.get(), completed_combo.get(), filter_window
            ),
        ).pack(pady=20)

    def apply_filter(self, priority, completed, window):
        """Apply the selected filter to the task list."""
        filtered_tasks = []

        # Get all tasks for the logged-in user
        tasks_to_filter = self.tasks.get(self.user, [])

        # Filter by priority
        if priority != "All":
            tasks_to_filter = [task for task in tasks_to_filter if task["priority"] == priority]

        # Filter by completion status
        if completed == "Completed":
            tasks_to_filter = [task for task in tasks_to_filter if task["completed"]]
        elif completed == "Pending":
            tasks_to_filter = [task for task in tasks_to_filter if not task["completed"]]

        # Refresh the task list with the filtered tasks
        self.refresh_task_list(filtered_tasks=tasks_to_filter)

        window.destroy()

    def refresh_task_list(self, filtered_tasks=None):
        """Refresh the task list display based on filtered tasks."""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # Use filtered tasks or show all tasks if no filter is applied
        tasks_to_display = filtered_tasks if filtered_tasks else self.tasks.get(self.user, [])

        for task in tasks_to_display:
            self.task_tree.insert(
                "",
                "end",
                values=(
                    task["name"],
                    task["priority"],
                    task["due_date"],
                    task["timestamp"],
                    "✔" if task["completed"] else "❌",
                ),
            )


# Main Function
def main():
    root = tk.Tk()
    app = TaskApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
