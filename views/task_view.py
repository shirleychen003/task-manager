import tkinter as tk
from tkinter import ttk
from views.edit_task_form import EditTaskForm
from tkinter import messagebox

class TaskView(tk.Frame):
    def __init__(self, parent, task_controller):
        super().__init__(parent)
        self.task_controller = task_controller
        self.create_widgets()
        self.refresh_tasks()
    
    def create_widgets(self):
        columns = ('ID', 'Title', 'Description', 'Deadline', 'Priority', 'Status')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Optional: Bind double-click to edit task
        self.tree.bind("<Double-1>", self.on_double_click)
    
    def refresh_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        tasks = self.task_controller.get_all_tasks()
        for task in tasks:
            deadline = task.deadline.strftime('%Y-%m-%d') if task.deadline else ''
            self.tree.insert('', tk.END, values=(task.id, task.title, task.description, deadline, task.priority, task.status))
    
    def get_selected_task(self):
        selected = self.tree.selection()
        if selected:
            task_id = self.tree.item(selected[0])['values'][0]
            tasks = self.task_controller.get_all_tasks()
            for task in tasks:
                if task.id == task_id:
                    return task
        return None
    
    def on_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            task_id = self.tree.item(selected_item[0])['values'][0]
            tasks = self.task_controller.get_all_tasks()
            for task in tasks:
                if task.id == task_id:
                    task_data = (
                        task.id,
                        task.title,
                        task.description,
                        task.deadline.strftime('%Y-%m-%d') if task.deadline else '',
                        task.priority,
                        task.status
                    )
                    edit_form = EditTaskForm(self, self.task_controller, task_data, on_task_updated=self.refresh_tasks)
                    edit_form.grab_set()
                    break 