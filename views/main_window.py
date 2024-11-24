import tkinter as tk
from tkinter import ttk
from controllers.task_controller import TaskController
from controllers.preferences_controller import PreferencesController
from views.task_form import TaskForm
from views.task_view import TaskView

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
        
        # Initialize Views
        self.task_view = TaskView(self, self.task_controller)
        self.task_view.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.task_form = TaskForm(self, self.task_controller, on_task_added=self.task_view.refresh_tasks)
        self.task_form.pack(side=tk.TOP, fill=tk.X)
    
    def create_menu(self):
        menubar = tk.Menu(self)
        
        # Preferences Menu
        preferences_menu = tk.Menu(menubar, tearoff=0)
        preferences_menu.add_command(label="Change Theme", command=self.change_theme)
        preferences_menu.add_command(label="Change Font Size", command=self.change_font_size)
        menubar.add_cascade(label="Preferences", menu=preferences_menu)
        
        self.config(menu=menubar)
    
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