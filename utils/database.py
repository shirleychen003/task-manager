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