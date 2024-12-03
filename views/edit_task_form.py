import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

class EditTaskForm(tk.Frame):
    def __init__(self, parent, task_controller, task, on_task_updated=None):
        super().__init__(parent)
        self.parent = parent
        self.task_controller = task_controller
        self.task = task
        self.on_task_updated = on_task_updated
        self.configure(bg='white')
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        tk.Label(self, text="Title:", bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.title_entry = tk.Entry(self, width=40)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)
        self.title_entry.insert(0, self.task.title)
        
        # Description
        tk.Label(self, text="Description:", bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.description_entry = tk.Entry(self, width=40)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)
        self.description_entry.insert(0, self.task.description)
        
        # Deadline
        tk.Label(self, text="Deadline (YYYY-MM-DD):", bg='white').grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.deadline_entry = tk.Entry(self, width=40)
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=10)
        deadline_str = self.task.deadline.strftime('%Y-%m-%d') if self.task.deadline else ''
        self.deadline_entry.insert(0, deadline_str)
        
        # Priority
        tk.Label(self, text="Priority:", bg='white').grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.priority_var = tk.StringVar(value=self.task.priority)
        ttk.Combobox(self, textvariable=self.priority_var, values=['High', 'Medium', 'Low'], state='readonly').grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        # Status
        tk.Label(self, text="Status:", bg='white').grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.status_var = tk.StringVar(value=self.task.status)
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
        
        if not title:
            messagebox.showerror("Invalid Input", "Title cannot be empty.")
            return
        
        # Handle deadline validation
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Please enter the deadline in YYYY-MM-DD format.\nExample: 2024-12-31"
                )
                return
        
        updated_data = {
            'title': title,
            'description': description,
            'deadline': deadline,
            'priority': priority,
            'status': status
        }
        
        self.task_controller.edit_task(self.task.id, updated_data)
        
        if self.on_task_updated:
            self.on_task_updated()
        
        messagebox.showinfo("Success", "Task updated successfully.")
        self.parent.destroy()