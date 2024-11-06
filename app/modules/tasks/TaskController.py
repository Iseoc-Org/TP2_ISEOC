from flask import request
from marshmallow import ValidationError
from app.modules.tasks.TaskService import TaskService
from app.modules.tasks.Taskdto import CreateTaskSchema, UpdateTaskSchema

create_task_schema = CreateTaskSchema()
update_task_schema = UpdateTaskSchema()

def get_all_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', type=str)
    
    tasks, total = TaskService.get_all_tasks(page=page, per_page=per_page, status=status)
    return {
        "tasks": [task.dict_for_json() for task in tasks],
        "total": total,
        "page": page,
        "per_page": per_page
    }


def get_task_by_id(task_id):
    task = TaskService.get_task_by_id(task_id)
    return task.dict_for_json() if task else ({"error": "Task not found"}, 404)

def create_task():
    try:
        data = create_task_schema.load(request.get_json())
    except ValidationError as err:
        return {"errors": err.messages}, 400

    task = TaskService.create_task(data)
    return task.to_dict(), 201

def bulk_add_tasks():
    try:
        tasks_data = request.json.get("tasks")
        tasks = [Task(**task) for task in tasks_data]
        db.session.bulk_save_objects(tasks)
        db.session.commit()
        return {"message": "Tasks added successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400

def bulk_delete_tasks():
    try:
        task_ids = request.json.get("task_ids")
        Task.query.filter(Task.id.in_(task_ids)).delete(synchronize_session=False)
        db.session.commit()
        return {"message": "Tasks deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400

def update_task(task_id):
    try:
        data = update_task_schema.load(request.get_json())
    except ValidationError as err:
        return {"errors": err.messages}, 400

    task = TaskService.update_task(task_id, data)
    return task.to_dict() if task else ({"error": "Task not found"}, 404)

def delete_task(task_id):
    success = TaskService.delete_task(task_id)
    return ('', 204) if success else ({"error": "Task not found"}, 404)

