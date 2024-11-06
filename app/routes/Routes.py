from app.modules.tasks.TaskRoutes import task_ns
from app import api

def register_blueprints(app):
    api.add_namespace(task_ns, path='/api/tasks')
