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