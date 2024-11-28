import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class EditTaskForm(tk.Frame):
    def __init__(self, parent, task_controller, task_data, on_task_updated=None):
        super().__init__(parent)
        self.parent = parent
        self.task_controller = task_controller
        self.task_id = task_data[0]
        self.on_task_updated = on_task_updated
        self.configure(bg='white')
        self.create_widgets(task_data)
    
    def create_widgets(self, task_data):
        # Title
        tk.Label(self, text="Title:", bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.title_entry = tk.Entry(self, width=40)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)
        self.title_entry.insert(0, task_data[1])
        
        # Description
        tk.Label(self, text="Description:", bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.description_entry = tk.Entry(self, width=40)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)
        self.description_entry.insert(0, task_data[2])
        
        # Deadline
        tk.Label(self, text="Deadline (YYYY-MM-DD):", bg='white').grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.deadline_entry = tk.Entry(self, width=40)
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=10)
        self.deadline_entry.insert(0, task_data[3])
        
        # Priority
        tk.Label(self, text="Priority:", bg='white').grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.priority_var = tk.StringVar(value=task_data[4])
        ttk.Combobox(self, textvariable=self.priority_var, values=['High', 'Medium', 'Low'], state='readonly').grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        # Status
        tk.Label(self, text="Status:", bg='white').grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.status_var = tk.StringVar(value=task_data[5])
        ttk.Combobox(self, textvariable=self.status_var, values=['Pending', 'Completed'], state='readonly').grid(row=4, column=1, padx=10, pady=10, sticky='w')
        
        # Update Task Button
        update_button = tk.Button(self, text="Update Task", command=self.update_task)
        update_button.grid(row=5, column=0, columnspan=2, pady=20)
    
    def update_task(self):
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        deadline_str = self.deadline_entry.get().strip()
        priority = self.priority_var.get()
        status = self.status_var.get()
        
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter the deadline in YYYY-MM-DD format.")
            return  # Prevent updating if the date is invalid
        
        if not title:
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
        self.parent.master.hide_overlay()
        
        # Refresh the task list
        if self.on_task_updated:
            self.on_task_updated()