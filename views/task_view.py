import tkinter as tk
from tkinter import ttk

class TaskView(tk.Frame):
    def __init__(self, parent, task_controller):
        super().__init__(parent)
        self.task_controller = task_controller
        self.create_widgets()
        self.refresh_tasks()
    
    def create_widgets(self):
        columns = ('ID', 'Title', 'Description', 'Deadline', 'Priority', 'Status')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Context Menu
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Mark as Complete", command=self.mark_complete)
        self.menu.add_command(label="Delete Task", command=self.delete_task)
    
    def refresh_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        tasks = self.task_controller.get_all_tasks()
        for task in tasks:
            deadline = task.deadline.strftime('%Y-%m-%d') if task.deadline else ''
            self.tree.insert('', tk.END, values=(task.id, task.title, task.description, deadline, task.priority, task.status))
    
    def show_context_menu(self, event):
        selected_item = self.tree.identify_row(event.y)
        if selected_item:
            self.tree.selection_set(selected_item)
            self.menu.post(event.x_root, event.y_root)
    
    def mark_complete(self):
        selected = self.tree.selection()
        if selected:
            task_id = self.tree.item(selected[0])['values'][0]
            self.task_controller.mark_task_complete(task_id)
            self.refresh_tasks()
    
    def delete_task(self):
        selected = self.tree.selection()
        if selected:
            task_id = self.tree.item(selected[0])['values'][0]
            self.task_controller.delete_task(task_id)
            self.refresh_tasks() 