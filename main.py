import sys
import threading
from views.task_manager_gui import TaskManagerGUI
from controllers.task_controller import TaskController
from utils.notifications import NotificationManager

def main():
    task_controller = TaskController()
    app = TaskManagerGUI(task_controller)
    
    # Initialize Notification Manager
    notification_manager = NotificationManager(task_controller)
    scheduler_thread = threading.Thread(target=notification_manager.run_scheduler, daemon=True)
    scheduler_thread.start()
    
    app.mainloop()
    notification_manager.stop_scheduler()

if __name__ == "__main__":
    main()