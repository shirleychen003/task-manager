import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from views.edit_task_form import EditTaskForm
from views.task_form import TaskForm

class TaskManagerGUI(tk.Tk):
    def __init__(self, task_controller):
        super().__init__()
        
        self.task_controller = task_controller
        
        # Window setup
        self.title("YOUR TASKS")
        
        # Allow window to resize based on content
        self.resizable(True, True)
        
        # Configure grid weight
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.configure(bg='#87CEFA')
        
        self.create_header()
        self.create_current_tasks_section()
        self.create_completed_tasks_section()
        
        # Initial refresh
        self.refresh_tasks()
    
    def create_header(self):
        header_frame = tk.Frame(self, bg='#87CEFA')
        header_frame.pack(fill='x', pady=20)
        
        title = tk.Label(
            header_frame, 
            text="DAVID'S TASKS",
            font=('Arial', 24, 'bold'),
            bg='#87CEFA'
        )
        title.pack()
        
        today = datetime.now().strftime("Today is %A, %B %d, %Y")
        date_label = tk.Label(
            header_frame,
            text=today,
            font=('Arial', 14),
            bg='#87CEFA'
        )
        date_label.pack()
    
    def create_current_tasks_section(self):
        tk.Label(
            self,
            text="Your Current Tasks:",
            font=('Arial', 18, 'bold'),
            bg='#87CEFA',
            anchor='w'
        ).pack(padx=20, pady=(20,10), anchor='w')
        
        # Sort Buttons Frame
        sort_frame = tk.Frame(self, bg='#87CEFA')
        sort_frame.pack(fill='x', padx=20)
        
        sort_label = tk.Label(sort_frame, text="Sort By:", bg='#4169E1', fg='white',
                              padx=20, pady=5, relief='flat')
        sort_label.pack(side='left', padx=(0,10))
        
        priority_btn = tk.Button(sort_frame, text="Priority", bg='#A9A9A9',
                                 command=self.sort_by_priority)
        priority_btn.pack(side='left', padx=5)
        
        date_btn = tk.Button(sort_frame, text="Date", bg='#A9A9A9',
                             command=self.sort_by_date)
        date_btn.pack(side='left', padx=5)
        
        # Tasks Treeview
        columns = ('ID', 'Title', 'Description', 'Deadline', 'Priority')
        self.current_tasks = ttk.Treeview(self, columns=columns, show='headings', height=5)
        
        # Configure columns
        for col in columns:
            self.current_tasks.heading(col, text=col)
            self.current_tasks.column(col, width=100)
        
        self.current_tasks.pack(fill='both', padx=20)
        
        # Action Buttons Frame
        action_frame = tk.Frame(self, bg='#87CEFA')
        action_frame.pack(fill='x', padx=20, pady=10)
        
        edit_btn = tk.Button(action_frame, text="Edit Task", bg='#B0C4DE',
                             command=self.edit_selected_task)
        edit_btn.pack(side='left', padx=5)
        
        delete_btn = tk.Button(action_frame, text="Delete Task", bg='#B0C4DE',
                               command=self.delete_selected_task)
        delete_btn.pack(side='left', padx=5)
    
    def create_completed_tasks_section(self):
        tk.Label(
            self,
            text="Completed Tasks:",
            font=('Arial', 18, 'bold'),
            bg='#87CEFA',
            anchor='w'
        ).pack(padx=20, pady=(20,10), anchor='w')
        
        # Completed Tasks Treeview
        columns = ('Title', 'Description', 'Completion Date')
        self.completed_tasks = ttk.Treeview(self, columns=columns, show='headings', height=5)
        
        for col in columns:
            self.completed_tasks.heading(col, text=col)
            self.completed_tasks.column(col, width=100)
        
        self.completed_tasks.pack(fill='both', padx=20)
        
        # Add Task Button
        add_task_btn = tk.Button(
            self, 
            text="Add a Task", 
            bg='#4169E1', 
            fg='black', 
            command=self.open_add_task_window
        )
        add_task_btn.pack(pady=20)
    
    def open_add_task_window(self):
        add_task_window = tk.Toplevel(self)
        add_task_window.title("Add New Task")
        add_task_window.configure(bg='#87CEFA')
        
        task_form = TaskForm(
            add_task_window, 
            self.task_controller, 
            on_task_added=self.refresh_tasks
        )
        task_form.pack(fill='both', expand=True)
    
    def refresh_tasks(self):
        # Clear current tasks
        for item in self.current_tasks.get_children():
            self.current_tasks.delete(item)
        
        # Fetch and insert current tasks
        tasks = self.task_controller.get_all_tasks()
        for task in tasks:
            if task.status == 'Pending':
                deadline_str = task.deadline.strftime('%Y-%m-%d') if task.deadline else ''
                self.current_tasks.insert('', 'end', values=(
                    task.id,
                    task.title,
                    task.description,
                    deadline_str,
                    task.priority
                ))
        
        # Clear completed tasks
        for item in self.completed_tasks.get_children():
            self.completed_tasks.delete(item)
        
        # Fetch and insert completed tasks
        for task in tasks:
            if task.status == 'Completed':
                completion_date = task.deadline.strftime('%Y-%m-%d') if task.deadline else ''
                self.completed_tasks.insert('', 'end', values=(
                    task.title,
                    task.description,
                    completion_date
                ))
    
    def sort_by_priority(self):
        tasks = self.task_controller.get_all_tasks()
        pending_tasks = [task for task in tasks if task.status == 'Pending']
        # Define a priority mapping to sort High > Medium > Low
        priority_mapping = {'High': 0, 'Medium': 1, 'Low': 2}
        sorted_tasks = sorted(pending_tasks, key=lambda t: priority_mapping.get(t.priority, 3))
        self._update_current_tasks_view(sorted_tasks)
    
    def sort_by_date(self):
        tasks = self.task_controller.get_all_tasks()
        pending_tasks = [task for task in tasks if task.status == 'Pending']
        sorted_tasks = sorted(pending_tasks, key=lambda t: t.deadline or datetime.max)
        self._update_current_tasks_view(sorted_tasks)
    
    def _update_current_tasks_view(self, tasks):
        # Clear current tasks
        for item in self.current_tasks.get_children():
            self.current_tasks.delete(item)
        
        # Insert sorted tasks
        for task in tasks:
            deadline_str = task.deadline.strftime('%Y-%m-%d') if task.deadline else ''
            self.current_tasks.insert('', 'end', values=(
                task.id,
                task.title,
                task.description,
                deadline_str,
                task.priority
            ))
    
    def edit_selected_task(self):
        selected_item = self.current_tasks.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a task to edit.")
            return
        
        task_id = self.current_tasks.item(selected_item)['values'][0]
        task = self.task_controller.get_task_by_id(task_id)
        
        if task:
            edit_task_window = tk.Toplevel(self)
            edit_task_window.title("Edit Task")
            edit_task_window.configure(bg='#87CEFA')
            
            edit_form = EditTaskForm(
                edit_task_window,
                self.task_controller,
                task,
                on_task_updated=self.refresh_tasks
            )
            edit_form.pack(fill='both', expand=True)
        else:
            messagebox.showerror("Error", "Task not found.")
    
    def delete_selected_task(self):
        selected_item = self.current_tasks.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return
        
        task_id = self.current_tasks.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
        if confirm:
            self.task_controller.delete_task(task_id)
            self.refresh_tasks()
    
    # Additional methods can be added as required
