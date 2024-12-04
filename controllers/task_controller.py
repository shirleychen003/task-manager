from models.task_model import Task
from utils.database import Database
from datetime import datetime

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
        if isinstance(updated_data.get('deadline'), datetime):
            updated_data['deadline'] = updated_data['deadline'].strftime('%Y-%m-%d')
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
    
    def get_task_by_id(self, task_id):
        tasks = self.get_all_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None
    
    def clear_all_tasks(self):
        self.db.clear_all_tasks()