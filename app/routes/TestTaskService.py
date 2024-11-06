import pytest
from app import create_app, db
from flask import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_add_task_missing_fields(client):
    response = client.post('/api/tasks', json={
        'title': 'Incomplete Task'
    })
    assert response.status_code == 400 

def test_add_task_invalid_status(client):

    response = client.post('/api/tasks', json={
        'title': 'Task with Invalid Status',
        'description': 'Testing invalid status',
        'status': 'INVALID_STATUS' 
    })
    assert response.status_code == 400  
def test_add_task_success(client):

    response = client.post('/api/tasks', json={
        'title': 'Test Task',
        'description': 'This is a test task',
        'status': 'PENDING'
    })
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['title'] == 'Test Task'
    assert data['description'] == 'This is a test task'
    assert data['status'] == 'PENDING'
