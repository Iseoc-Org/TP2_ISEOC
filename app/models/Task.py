from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class Task(db.Model):
    __tablename__ = 'Tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.PENDING)

    def dict_for_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value 
        }
