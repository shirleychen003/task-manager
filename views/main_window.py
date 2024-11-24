import tkinter as tk
from tkinter import ttk
from controllers.task_controller import TaskController
from controllers.preferences_controller import PreferencesController
from views.task_form import TaskForm
from views.task_view import TaskView
from views.edit_task_form import EditTaskForm

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Accessible Task Manager")
        self.geometry("800x600")
        
        # Initialize Controllers
        self.task_controller = TaskController()
        self.preferences_controller = PreferencesController()
        
        # Initialize Preferences
        self.preferences_controller.load_preferences()
        self.apply_preferences()
        
        # Set up menu
        self.create_menu()
        
        # Initialize Task View
        self.task_view = TaskView(self, self.task_controller)
        self.task_view.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Initialize Task Form
        self.task_form = TaskForm(self, self.task_controller, on_task_added=self.task_view.refresh_tasks)
        self.task_form.pack(side=tk.TOP, fill=tk.X)
        
        # Initialize Action Buttons
        self.create_action_buttons()
    
    def create_menu(self):
        menubar = tk.Menu(self)
        
        # Preferences Menu
        preferences_menu = tk.Menu(menubar, tearoff=0)
        preferences_menu.add_command(label="Change Theme", command=self.change_theme)
        preferences_menu.add_command(label="Change Font Size", command=self.change_font_size)
        menubar.add_cascade(label="Preferences", menu=preferences_menu)
        
        self.config(menu=menubar)
    
    def create_action_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        edit_button = tk.Button(button_frame, text="Edit Task", command=self.edit_task)
        edit_button.pack(side=tk.LEFT, padx=10)
        
        delete_button = tk.Button(button_frame, text="Delete Task", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, padx=10)
    
    def change_theme(self):
        # Implement theme change
        new_theme = 'Dark' if self.preferences_controller.preferences.theme == 'Light' else 'Light'
        self.preferences_controller.apply_theme(new_theme)
        self.apply_preferences()
    
    def change_font_size(self):
        # Implement font size change
        new_size = self.preferences_controller.preferences.font_size + 2
        self.preferences_controller.change_font_size(new_size)
        self.apply_preferences()
    
    def apply_preferences(self):
        prefs = self.preferences_controller.preferences
        # Apply theme
        bg_color = 'white' if prefs.theme == 'Light' else 'gray20'
        fg_color = 'black' if prefs.theme == 'Light' else 'white'
        self.configure(bg=bg_color)
        
        # Apply font size
        default_font = ('Arial', prefs.font_size)
        for widget in self.winfo_children():
            try:
                widget.configure(font=default_font, bg=bg_color, fg=fg_color)
            except:
                pass  # Some widgets may not support these options
    
    def get_selected_task(self):
        selected = self.task_view.get_selected_task()
        return selected
    
    def edit_task(self):
        selected_task = self.get_selected_task()
        if selected_task:
            task_data = (
                selected_task.id,
                selected_task.title,
                selected_task.description,
                selected_task.deadline.strftime('%Y-%m-%d') if selected_task.deadline else '',
                selected_task.priority,
                selected_task.status
            )
            edit_form = EditTaskForm(self, self.task_controller, task_data, on_task_updated=self.task_view.refresh_tasks)
            edit_form.grab_set()
        else:
            tk.messagebox.showwarning("No Selection", "Please select a task to edit.")
    
    def delete_task(self):
        selected_task = self.get_selected_task()
        if selected_task:
            confirm = tk.messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
            if confirm:
                self.task_controller.delete_task(selected_task.id)
                self.task_view.refresh_tasks()
        else:
            tk.messagebox.showwarning("No Selection", "Please select a task to delete.")