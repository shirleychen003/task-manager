import tkinter as tk
from tkinter import ttk

class Visualization:
    def __init__(self, parent, task_controller):
        self.parent = parent
        self.task_controller = task_controller
        self.create_widgets()
    
    def create_widgets(self):
        self.tree = ttk.Treeview(self.parent, columns=('Priority', 'Count'), show='headings')
        self.tree.heading('Priority', text='Priority')
        self.tree.heading('Count', text='Count')
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.generate_progress_chart()
    
    def generate_progress_chart(self):
        tasks = self.task_controller.get_all_tasks()
        priority_count = {'High':0, 'Medium':0, 'Low':0}
        for task in tasks:
            if task.priority in priority_count:
                priority_count[task.priority] += 1
        for priority, count in priority_count.items():
            self.tree.insert('', tk.END, values=(priority, count)) 