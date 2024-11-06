from flask_restx import Namespace, Resource, fields
from app.modules.tasks import TaskController

task_ns = Namespace('tasks', description='Task operations')

task_model = task_ns.model('Task', {
    'id': fields.Integer(readOnly=True, description='Unique identifier'),
    'title': fields.String(required=True, description='Title of the task'),
    'description': fields.String(required=True, description='Task description'),
    'status': fields.String(description='Task status')
})

@task_ns.route('/')
class TaskList(Resource):
    @task_ns.doc('list_tasks')
    def get(self):
        response = task_controller.get_all_tasks()
        return response 
 
    @task_ns.expect(task_model)
    @task_ns.doc('create_task')
    @task_ns.marshal_with(task_model, code=201)
    def post(self):
        return task_controller.create_task()


@task_ns.route('/')
class TaskList(Resource):
    @verifyToken
    def get(self):
        response = task_controller.get_all_tasks()
        return response 

    @task_ns.expect(task_model)
    @task_ns.doc('create_task')
    @verifyToken
    @verifyRole('admin')  
    def post(self):
        return task_controller.create_task()

@task_ns.route('/<int:task_id>')
@task_ns.response(404, 'Task not found')
@task_ns.param('task_id', 'The task identifier')
class Task(Resource):
    @task_ns.doc('get_task')
    @task_ns.marshal_with(task_model)
    def get(self, task_id):
        return task_controller.get_task_by_id(task_id)

    @task_ns.expect(task_model)
    @task_ns.doc('update_task')
    @task_ns.marshal_with(task_model)
    def put(self, task_id):
        return task_controller.update_task(task_id)

    @task_ns.doc('delete_task')
    def delete(self, task_id):
        return task_controller.delete_task(task_id)

bulk_add_model = task_ns.model('BulkAdd', {
    'tasks': fields.List(fields.Nested(task_model), required=True, description='List of tasks to add')
})

bulk_delete_model = task_ns.model('BulkDelete', {
    'task_ids': fields.List(fields.Integer, required=True, description='List of task IDs to delete')
})


@task_ns.route('/bulk_add')
class BulkAddTasks(Resource):
    @task_ns.expect(bulk_add_model)
    @task_ns.doc('bulk_add_tasks')
    def post(self):
        tasks_data = task_ns.payload.get("tasks", [])
        return task_controller.bulk_add_tasks(tasks_data)

@task_ns.route('/bulk_delete')
class BulkDeleteTasks(Resource):
    @task_ns.expect(bulk_delete_model)
    @task_ns.doc('bulk_delete_tasks')
    def delete(self):
        task_ids = task_ns.payload.get("task_ids", [])
        return task_controller.bulk_delete_tasks(task_ids)
