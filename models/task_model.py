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