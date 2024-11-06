from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

db = SQLAlchemy()
api = Api()

def load_environment():
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        load_dotenv('.env.production')
    else:
        load_dotenv('.env.development')

load_environment()

from app.models.task import Task

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
        f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    api.init_app(app)
    CORS(app)

    from app.routes.routes import register_blueprints
    register_blueprints(app)

    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    with app.app_context():
        try:
            db.create_all()
            print("Success of table creation")
            showData()
        except Exception as e:
            print("Error in the creation of table", e)

    return app

def showData():
    if not Task.query.first():
        task1 = Task(title="First Task", description="This is the first task", status="PENDING")
        task2 = Task(title="Second Task", description="This is the second task", status="DONE")
        db.session.add_all([task1, task2])
        db.session.commit()
        print("Seed data inserted.")
    else:
        print("Data already exists, skipping seeding.")
