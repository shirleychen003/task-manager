from controllers.task_controller import TaskController

def clear_database():
    controller = TaskController()
    controller.clear_all_tasks()
    print("Database cleared successfully!")

if __name__ == "__main__":
    clear_database() 