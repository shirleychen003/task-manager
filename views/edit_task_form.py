import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox

class EditTaskForm(tk.Toplevel):
    def __init__(self, parent, task_controller, task_data, on_task_updated=None):
        super().__init__(parent)
        self.title("Edit Task")
        self.geometry("400x300")
        self.task_controller = task_controller
        self.task_id = task_data[0]
        self.on_task_updated = on_task_updated
        self.create_widgets(task_data)
    
    def create_widgets(self, task_data):
        # Title
        tk.Label(self, text="Title:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)
        self.title_entry.insert(0, task_data[1])
        
        # Description
        tk.Label(self, text="Description:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)
        self.description_entry.insert(0, task_data[2])
        
        # Deadline
        tk.Label(self, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.deadline_entry = tk.Entry(self)
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=10)
        self.deadline_entry.insert(0, task_data[3])
        
        # Priority
        tk.Label(self, text="Priority:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.priority_var = tk.StringVar(value=task_data[4])
        ttk.Combobox(self, textvariable=self.priority_var, values=['High', 'Medium', 'Low']).grid(row=3, column=1, padx=10, pady=10)
        
        # Status
        tk.Label(self, text="Status:").grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.status_var = tk.StringVar(value=task_data[5])
        ttk.Combobox(self, textvariable=self.status_var, values=['Pending', 'Completed']).grid(row=4, column=1, padx=10, pady=10)
        
        # Update Task Button
        update_button = tk.Button(self, text="Update Task", command=self.update_task)
        update_button.grid(row=5, column=0, columnspan=2, pady=20)
    
    def update_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        deadline_str = self.deadline_entry.get()
        priority = self.priority_var.get()
        status = self.status_var.get()
        
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter the deadline in YYYY-MM-DD format.")
            return  # Prevent updating if the date is invalid
        
        if not title.strip():
            messagebox.showerror("Invalid Input", "Title cannot be empty.")
            return
        
        updated_data = {
            'title': title,
            'description': description,
            'deadline': deadline,
            'priority': priority,
            'status': status
        }
        
        self.task_controller.edit_task(self.task_id, updated_data)
        
        # Close the edit form
        self.destroy()
        
        # Refresh the task list
        if self.on_task_updated:
            self.on_task_updated()