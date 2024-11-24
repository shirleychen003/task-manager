# Task Manager Project

## Overview

The **Task Manager Project** is an accessible and user-friendly task management application developed in Python, following the Model-View-Controller (MVC) architecture. Designed to help users organize, prioritize, and manage their tasks efficiently, the application emphasizes accessibility to cater to a wide range of users, including those with visual impairments.

## Features

- **Add, Edit, and Delete Tasks:** Easily manage your tasks with a straightforward interface.
- **Task Prioritization:** Assign priorities (High, Medium, Low) to tasks to focus on what's important.
- **Deadline Management:** Set deadlines for tasks and receive timely notifications.
- **Accessible Design:** High-contrast themes, adjustable font sizes, and minimalist layouts for better usability.
- **Notifications:** Receive reminders for upcoming task deadlines.
- **Progress Visualization:** View task statistics and progress through intuitive charts.

## Project Structure

The project is organized into modular components adhering to the MVC (Model-View-Controller) pattern, ensuring scalability and maintainability.

```
project/
├── main.py
├── models/
│ ├── __init__.py
│ ├── task_model.py
│ └── preferences_model.py
├── views/
│ ├── __init__.py
│ ├── main_window.py
│ ├── task_form.py
│ └── task_view.py
├── controllers/
│ ├── __init__.py
│ ├── task_controller.py
│ └── preferences_controller.py
├── utils/
│ ├── __init__.py
│ ├── database.py
│ ├── notifications.py
│ └── visualizations.py
├── resources/
│ └── (static resources like icons and stylesheets)
└── README.md
```

### Directory Breakdown

- **main.py:**  
  The entry point of the application. Initializes the main window and notification manager.

- **models/:**  
  Contains data models representing the core data structures.
  
  - `__init__.py`: Makes the `models` directory a Python package.
  - `task_model.py`: Defines the `Task` class representing a task entity.
  - `preferences_model.py`: Defines the `Preferences` class managing user settings.

- **views/:**  
  Contains GUI components built using Tkinter.
  
  - `__init__.py`: Makes the `views` directory a Python package.
  - `main_window.py`: Sets up the main application window and integrates other views.
  - `task_form.py`: Provides a form for adding and editing tasks.
  - `task_view.py`: Displays the list of tasks in a tabular format.

- **controllers/:**  
  Contains application logic handling the interaction between models and views.
  
  - `__init__.py`: Makes the `controllers` directory a Python package.
  - `task_controller.py`: Manages task-related operations such as adding, editing, and deleting tasks.
  - `preferences_controller.py`: Manages user preferences and applies settings to the UI.

- **utils/:**  
  Provides utility modules supporting various functionalities.
  
  - `__init__.py`: Makes the `utils` directory a Python package.
  - `database.py`: Handles database connections and operations using SQLite.
  - `notifications.py`: Manages scheduling and sending task reminders.
  - `visualizations.py`: Generates visual representations of task progress.


## Getting Started

### Prerequisites

- **Python 3.x**  
  Ensure you have Python 3 installed on your machine. You can download it from the [official website](https://www.python.org/downloads/).

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/task-manager.git
   cd task-manager
   ```

2. **Ensure Required Libraries are Installed**

   The application primarily uses Python's standard library and Tkinter for GUI. Tkinter typically comes pre-installed with Python. If not, install it via your package manager.

   - **For Windows:**  
     Tkinter is included with Python installations.

   - **For macOS:**  
     ```bash
     brew install python-tk
     ```

   - **For Linux (Debian/Ubuntu):**  
     ```bash
     sudo apt-get install python3-tk
     ```

### Running the Application

Navigate to the project directory and execute the `main.py` script:

```bash
python main.py
```

This will launch the Task Manager application window, where you can start adding and managing your tasks.

## Usage

1. **Adding a Task:**
   - Fill in the task details in the **Task Form** at the top of the window.
   - Click the **"Add Task"** button to save the task. The task list below will update automatically.

2. **Viewing Tasks:**
   - The **Task View** displays all tasks in a table format, showing details like Title, Description, Deadline, Priority, and Status.

3. **Managing Tasks:**
   - **Mark as Complete:** Right-click on a task and select **"Mark as Complete"** to update its status.
   - **Delete Task:** Right-click on a task and select **"Delete Task"** to remove it from the list.

4. **Preferences:**
   - Access the **Preferences** menu from the menu bar to change themes and adjust font sizes for better accessibility.

## Codebase Explanation

### Models

#### Task Model (`models/task_model.py`)

Defines the `Task` class representing a task with attributes like title, description, deadline, priority, and status.

```python:models/task_model.py
class Task:
    def __init__(self, id, title, description, deadline, priority='Low', status='Pending'):
        self.id = id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status

    def mark_complete(self):
        self.status = 'Completed'
```

#### Preferences Model (`models/preferences_model.py`)

Manages user preferences such as theme, font size, and color scheme, allowing them to be saved and loaded.

```python:models/preferences_model.py
import json
import os

class Preferences:
    def __init__(self, theme='Light', font_size=12, color_scheme='Default'):
        self.theme = theme
        self.font_size = font_size
        self.color_scheme = color_scheme

    def save_preferences(self, file_path='utils/preferences.json'):
        preferences = {
            'theme': self.theme,
            'font_size': self.font_size,
            'color_scheme': self.color_scheme
        }
        with open(file_path, 'w') as f:
            json.dump(preferences, f)

    def load_preferences(self, file_path='utils/preferences.json'):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                preferences = json.load(f)
                self.theme = preferences.get('theme', 'Light')
                self.font_size = preferences.get('font_size', 12)
                self.color_scheme = preferences.get('color_scheme', 'Default')
```

### Views

#### Main Window (`views/main_window.py`)

Sets up the main application window, integrates the task form and task view, and manages the application menu for preferences.

```python:views/main_window.py
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
```

#### Task Form (`views/task_form.py`)

Provides a form for users to input task details and add new tasks to the task list.

```python:views/task_form.py
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
```

#### Task View (`views/task_view.py`)

Displays the list of tasks in a table and provides context menu options to manage tasks.

```python:views/task_view.py
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
```

### Controllers

#### Task Controller (`controllers/task_controller.py`)

Handles all task-related operations, interfacing between the views and the database.

```python:controllers/task_controller.py
from models.task_model import Task
from utils.database import Database

class TaskController:
    def __init__(self):
        self.db = Database()
        self.db.create_tasks_table()
    
    def add_task(self, task_data):
        task = Task(
            id=None,
            title=task_data['title'],
            description=task_data['description'],
            deadline=task_data['deadline'],
            priority=task_data.get('priority', 'Low'),
            status='Pending'
        )
        self.db.insert_task(task)
    
    def edit_task(self, task_id, updated_data):
        self.db.update_task(task_id, updated_data)
    
    def delete_task(self, task_id):
        self.db.delete_task(task_id)
    
    def mark_task_complete(self, task_id):
        self.db.update_task(task_id, {'status': 'Completed'})
    
    def get_tasks_by_date(self, date):
        return self.db.get_tasks_by_deadline(date)
    
    def get_tasks_by_priority(self, priority):
        return self.db.get_tasks_by_priority(priority)
    
    def get_all_tasks(self):
        return self.db.get_all_tasks()
```

#### Preferences Controller (`controllers/preferences_controller.py`)

Manages user preferences and applies them to the application's UI.

```python:controllers/preferences_controller.py
from models.preferences_model import Preferences

class PreferencesController:
    def __init__(self):
        self.preferences = Preferences()
    
    def apply_theme(self, theme):
        self.preferences.theme = theme
        self.preferences.save_preferences()
    
    def change_font_size(self, size):
        self.preferences.font_size = size
        self.preferences.save_preferences()
    
    def update_color_scheme(self, scheme):
        self.preferences.color_scheme = scheme
        self.preferences.save_preferences()
    
    def load_preferences(self):
        self.preferences.load_preferences()
```

### Utilities

#### Database Utility (`utils/database.py`)

Handles all database operations using SQLite, including creating tables and CRUD operations.

```python:utils/database.py
import sqlite3
from models.task_model import Task
from datetime import datetime

class Database:
    def __init__(self, db_path='utils/tasks.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def create_tasks_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                deadline TEXT,
                priority TEXT DEFAULT 'Low',
                status TEXT DEFAULT 'Pending'
            )
        ''')
        self.conn.commit()
    
    def insert_task(self, task):
        deadline = task.deadline.strftime('%Y-%m-%d') if task.deadline else None
        self.cursor.execute('''
            INSERT INTO tasks (title, description, deadline, priority, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (task.title, task.description, deadline, task.priority, task.status))
        self.conn.commit()
    
    def update_task(self, task_id, updated_data):
        fields = ', '.join(f"{key}=?" for key in updated_data.keys())
        values = list(updated_data.values())
        values.append(task_id)
        query = f"UPDATE tasks SET {fields} WHERE id=?"
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def delete_task(self, task_id):
        self.cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        self.conn.commit()
    
    def get_tasks_by_deadline(self, date):
        self.cursor.execute('SELECT * FROM tasks WHERE deadline=?', (date.strftime('%Y-%m-%d'),))
        rows = self.cursor.fetchall()
        return [self.row_to_task(row) for row in rows]
    
    def get_tasks_by_priority(self, priority):
        self.cursor.execute('SELECT * FROM tasks WHERE priority=?', (priority,))
        rows = self.cursor.fetchall()
        return [self.row_to_task(row) for row in rows]
    
    def get_all_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        rows = self.cursor.fetchall()
        return [self.row_to_task(row) for row in rows]
    
    def row_to_task(self, row):
        deadline = datetime.strptime(row[3], '%Y-%m-%d') if row[3] else None
        return Task(
            id=row[0],
            title=row[1],
            description=row[2],
            deadline=deadline,
            priority=row[4],
            status=row[5]
        )
```

#### Notifications Utility (`utils/notifications.py`)

Manages scheduling and sending notifications for upcoming task deadlines.

```python:utils/notifications.py
import threading
import time
from datetime import datetime, timedelta

class NotificationManager:
    def __init__(self, task_controller):
        self.task_controller = task_controller
        self.running = False
    
    def schedule_notification(self, task):
        if task.deadline:
            notification_time = task.deadline - timedelta(minutes=30)  # 30 minutes before deadline
            delay = (notification_time - datetime.now()).total_seconds()
            if delay > 0:
                threading.Timer(delay, self.notify, args=(task,)).start()
    
    def notify(self, task):
        print(f"Reminder: Task '{task.title}' is due at {task.deadline}")
    
    def run_scheduler(self):
        self.running = True
        while self.running:
            tasks = self.task_controller.get_all_tasks()
            for task in tasks:
                if task.status == 'Pending':
                    self.schedule_notification(task)
            time.sleep(60)  # Check every minute
    
    def stop_scheduler(self):
        self.running = False
```

#### Visualizations Utility (`utils/visualizations.py`)

Generates visual representations of task progress and statistics.

```python:utils/visualizations.py
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
```

### Entry Point

#### Main (`main.py`)

Initializes the main window and starts the notification scheduler.

```python:main.py
import sys
import threading
from views.main_window import MainWindow
from utils.notifications import NotificationManager

def main():
    app = MainWindow()
    
    # Initialize Notification Manager
    notification_manager = NotificationManager(app.task_controller)
    scheduler_thread = threading.Thread(target=notification_manager.run_scheduler, daemon=True)
    scheduler_thread.start()
    
    app.mainloop()
    notification_manager.stop_scheduler()

if __name__ == '__main__':
    main()
```

## Accessibility Features

- **Themes and Stylesheets:**  
  Offers light and dark themes to accommodate different visual preferences and reduce eye strain.

- **Adjustable Font Sizes:**  
  Users can increase or decrease font sizes for better readability.

- **High-Contrast Options:**  
  High-contrast color schemes are available to enhance visibility for users with visual impairments.

- **Minimalist Design:**  
  A clean and simple interface reduces cognitive load and enhances focus.

## Testing

The project includes unit tests to ensure the reliability and correctness of models, controllers, and utilities.

### Running Tests

1. **Navigate to the Project Directory**

   ```bash
   cd project
   ```

2. **Run Tests Using `unittest`**

   ```bash
   python -m unittest discover tests
   ```

   This command discovers and runs all test cases within the `tests/` directory.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- **Python Tkinter Documentation:**  
  Comprehensive documentation for building GUIs with Tkinter.
  
- **Python Standard Library:**  
  Leveraged various modules like `sqlite3`, `threading`, and `json` to build robust functionalities.
  
- **INF452 Class:**  
  Inspired by coursework and project guidelines from the INF452 class.
