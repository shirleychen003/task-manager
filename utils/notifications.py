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