import sqlite3
import threading
from models.task_model import Task
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    _local = threading.local()
    
    def __init__(self, db_path='utils/tasks.db'):
        self.db_path = db_path
        self._init_connection()
        logging.debug(f"Database initialized with path: {self.db_path}")
    
    def _init_connection(self):
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_path)
            self._local.cursor = self._local.connection.cursor()
    
    @property
    def conn(self):
        self._init_connection()
        return self._local.connection
    
    @property
    def cursor(self):
        self._init_connection()
        return self._local.cursor
    
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
        try:
            deadline = task.deadline.strftime('%Y-%m-%d') if task.deadline else None
            self.cursor.execute('''
                INSERT INTO tasks (title, description, deadline, priority, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (task.title, task.description, deadline, task.priority, task.status))
            self.conn.commit()
            logging.debug(f"Inserted task: {task.title}")
        except sqlite3.Error as e:
            logging.error(f"Error inserting task: {e}")
    
    def update_task(self, task_id, updated_data):
        try:
            fields = ', '.join(f"{key}=?" for key in updated_data.keys())
            values = list(updated_data.values())
            values.append(task_id)
            query = f"UPDATE tasks SET {fields} WHERE id=?"
            self.cursor.execute(query, values)
            self.conn.commit()
            logging.debug(f"Task ID {task_id} updated with {updated_data}")
        except sqlite3.Error as e:
            logging.error(f"Failed to update task ID {task_id}: {e}")
    
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