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