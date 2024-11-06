from app.models.Task import Task, TaskStatus, db

class TaskService:
    @staticmethod
    def create_task(data):
        task = Task(title=data['title'], description=data['description'], status=data.get('status', TaskStatus.PENDING))
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def update_task(task_id, data):
        task = Task.query.get(task_id)
        if not task:
            return None
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        db.session.commit()
        return task

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return None
        db.session.delete(task)
        db.session.commit()
        return True
    @staticmethod
    def get_all_tasks(page=1, per_page=10, status=None):
        query = Task.query

        if status:
            query = query.filter_by(status=status)
        
        tasks = query.paginate(page=page, per_page=per_page, error_out=False)
        return tasks.items, tasks.total

    @staticmethod
    def get_task_by_id(task_id):
        return Task.query.get(task_id)    
