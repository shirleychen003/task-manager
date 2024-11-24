import tkinter as tk
from tkinter import ttk
from datetime import datetime

class TaskForm(tk.Frame):
    def __init__(self, parent, task_controller, on_task_added=None):
        super().__init__(parent)
        self.task_controller = task_controller
        self.on_task_added = on_task_added
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        tk.Label(self, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Description
        tk.Label(self, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Deadline
        tk.Label(self, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.deadline_entry = tk.Entry(self)
        self.deadline_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Priority
        tk.Label(self, text="Priority:").grid(row=3, column=0, padx=5, pady=5)
        self.priority_var = tk.StringVar(value='Low')
        ttk.Combobox(self, textvariable=self.priority_var, values=['High', 'Medium', 'Low']).grid(row=3, column=1, padx=5, pady=5)
        
        # Add Task Button
        add_button = tk.Button(self, text="Add Task", command=self.add_task)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        deadline_str = self.deadline_entry.get()
        priority = self.priority_var.get()
        
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        except ValueError:
            deadline = None  # Handle invalid date format as needed
        
        task_data = {
            'title': title,
            'description': description,
            'deadline': deadline,
            'priority': priority
        }
        
        self.task_controller.add_task(task_data)
        
        # Clear fields after adding
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.priority_var.set('Low')
        
        # Invoke the callback to refresh the task list
        if self.on_task_added:
            self.on_task_added() 