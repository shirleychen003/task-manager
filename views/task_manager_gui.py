import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from views.edit_task_form import EditTaskForm

class TaskManagerGUI(tk.Tk):
    def __init__(self, task_controller):
        super().__init__()
        
        self.task_controller = task_controller
        
        # Window setup
        self.title("YOUR TASKS")
        
        # Calculate window size and position
        window_width = 1400
        window_height = 1080
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Center position
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Set geometry with position
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        # Allow window to resize based on content
        self.resizable(True, True)
        
        # Configure grid weight
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.configure(bg='#87CEFA')
        
        self.create_header()
        self.create_current_tasks_section()
        self.create_completed_tasks_section()
        self.create_add_task_section()
        
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
        
        # Tasks Treeview (instead of Listbox for better organization)
        columns = ('Title', 'Description', 'Deadline', 'Priority')
        self.current_tasks = ttk.Treeview(self, columns=columns, show='headings', height=5)
        
        # Configure columns
        for col in columns:
            self.current_tasks.heading(col, text=col)
            self.current_tasks.column(col, width=100)
        
        self.current_tasks.pack(fill='x', padx=20, pady=10)
        
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
            text="Completed Tasks!",
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
        
        self.completed_tasks.pack(fill='x', padx=20, pady=10)

    def create_add_task_section(self):
        # Create a frame with padding at the bottom
        add_task_frame = tk.Frame(self, bg='#87CEFA')
        add_task_frame.pack(fill='x', padx=20, pady=(20,40))  # Added bottom padding
        
        tk.Label(
            add_task_frame,
            text="Add a Task:",
            font=('Arial', 18, 'bold'),
            bg='#87CEFA',
            anchor='w'
        ).pack(pady=(0,10), anchor='w')
        
        form_frame = tk.Frame(add_task_frame, bg='#87CEFA')
        form_frame.pack(fill='x', pady=10)
        
        # Title
        tk.Label(form_frame, text="Title:", bg='#87CEFA', anchor='w').pack(fill='x')
        self.title_entry = tk.Entry(form_frame, bg='#E0E0E0')
        self.title_entry.pack(fill='x', pady=(0,10))
        
        # Description
        tk.Label(form_frame, text="Description:", bg='#87CEFA', anchor='w').pack(fill='x')
        self.desc_entry = tk.Entry(form_frame, bg='#E0E0E0')
        self.desc_entry.pack(fill='x', pady=(0,10))
        
        # Deadline
        tk.Label(form_frame, text="Deadline (YYYY-MM-DD):", bg='#87CEFA', anchor='w').pack(fill='x')
        self.deadline_entry = tk.Entry(form_frame, bg='#E0E0E0')
        self.deadline_entry.pack(fill='x', pady=(0,10))
        
        # Priority
        tk.Label(form_frame, text="Priority:", bg='#87CEFA', anchor='w').pack(fill='x')
        self.priority_combo = ttk.Combobox(form_frame, values=['High', 'Medium', 'Low'])
        self.priority_combo.set('Low')
        self.priority_combo.pack(fill='x', pady=(0,10))
        
        # Add Task Button - with bottom padding
        tk.Button(
            form_frame, 
            text="Add Task", 
            command=self.add_task,
            bg='#4169E1',
            fg='black',
            pady=5
        ).pack(pady=(10,20))
        self.title_entry.pack(fill='x', pady=(0,10))
        

    def refresh_tasks(self):
        # Clear current tasks
        for item in self.current_tasks.get_children():
            self.current_tasks.delete(item)
        
        # Clear completed tasks
        for item in self.completed_tasks.get_children():
            self.completed_tasks.delete(item)
        
        # Refresh with new data
        tasks = self.task_controller.get_all_tasks()
        for task in tasks:
            deadline = task.deadline.strftime('%Y-%m-%d') if task.deadline else ''
            
            if task.status == 'Pending':
                self.current_tasks.insert('', 'end', values=(
                    task.title, task.description, deadline, task.priority
                ))
            else:
                self.completed_tasks.insert('', 'end', values=(
                    task.title, task.description, deadline
                ))

    def add_task(self):
        try:
            task_data = {
                'title': self.title_entry.get(),
                'description': self.desc_entry.get(),
                'deadline': datetime.strptime(self.deadline_entry.get(), '%Y-%m-%d'),
                'priority': self.priority_combo.get()
            }
            
            if not task_data['title']:
                messagebox.showerror("Error", "Title is required!")
                return
            
            self.task_controller.add_task(task_data)
            self.refresh_tasks()
            
            # Clear form
            self.title_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.deadline_entry.delete(0, tk.END)
            self.priority_combo.set('Low')
            
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")

    def sort_by_priority(self):
        print("sort_by_priority called.")
        priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
        
        try:
            # Get fresh data from database
            self.refresh_tasks()
            
            # Get current items
            items = [self.current_tasks.item(item)['values'] for item in self.current_tasks.get_children()]
            print(f"Unsorted items: {items}")
            
            # Sort items
            sorted_items = sorted(items, key=lambda x: priority_order.get(x[4], 4) if x and len(x) > 4 else 4)
            print(f"Sorted items: {sorted_items}")
            
            # Clear and reinsert
            self.current_tasks.delete(*self.current_tasks.get_children())
            
            # Insert sorted items
            for task in sorted_items:
                self.current_tasks.insert('', 'end', values=task)
            
            # Force visual update
            self.update_idletasks()
            print("sort_by_priority completed successfully.")
        
        except Exception as e:
            print(f"Error in sort_by_priority: {e}")
            messagebox.showerror("Sort Error", f"An error occurred while sorting by priority: {e}")

    def sort_by_date(self):
        print("sort_by_date called.")
        
        try:
            # Get fresh data from database
            self.refresh_tasks()
            
            # Get current items
            items = [self.current_tasks.item(item)['values'] for item in self.current_tasks.get_children()]
            print(f"Unsorted items: {items}")
            
            # Sort items
            sorted_items = sorted(
                items,
                key=lambda x: datetime.strptime(x[3], '%Y-%m-%d') if x and len(x) > 3 and x[3] else datetime.max
            )
            print(f"Sorted items: {sorted_items}")
            
            # Clear and reinsert
            self.current_tasks.delete(*self.current_tasks.get_children())
            
            # Insert sorted items
            for task in sorted_items:
                self.current_tasks.insert('', 'end', values=task)
            
            # Force visual update
            self.update_idletasks()
            print("sort_by_date completed successfully.")
        
        except Exception as e:
            print(f"Error in sort_by_date: {e}")
            messagebox.showerror("Sort Error", f"An error occurred while sorting by date: {e}")

    def edit_selected_task(self):
        selected = self.current_tasks.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to edit")
            return
        
        task_id = self.current_tasks.item(selected[0])['values'][0]
        task = self.task_controller.get_task_by_id(task_id)
        
        if task:
            # Create edit window
            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Task")
            edit_window.geometry("400x400")
            
            # Convert task to tuple format expected by EditTaskForm
            task_data = (
                task.id,
                task.title,
                task.description,
                task.deadline.strftime('%Y-%m-%d') if task.deadline else '',
                task.priority,
                task.status
            )
            
            # Create and pack the edit form
            edit_form = EditTaskForm(
                edit_window, 
                self.task_controller, 
                task_data,
                on_task_updated=self.refresh_tasks
            )
            edit_form.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Make window modal
            edit_window.transient(self)
            edit_window.grab_set()
            
            # Center the window
            edit_window.update_idletasks()
            width = edit_window.winfo_width()
            height = edit_window.winfo_height()
            x = (edit_window.winfo_screenwidth() // 2) - (width // 2)
            y = (edit_window.winfo_screenheight() // 2) - (height // 2)
            edit_window.geometry(f'{width}x{height}+{x}+{y}')

    def delete_selected_task(self):
        selected = self.current_tasks.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to delete")
            return
        
        task_id = self.current_tasks.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            self.task_controller.delete_task(task_id)
            self.refresh_tasks()
