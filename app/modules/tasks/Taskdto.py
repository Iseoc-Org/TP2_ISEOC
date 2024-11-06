from marshmallow import Schema, fields, validate, post_load
from app.models.Task import TaskStatus

class CreateTaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    status = fields.Str(validate=validate.OneOf([status.value for status in TaskStatus]))

class UpdateTaskSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(min=1, max=255))
    status = fields.Str(validate=validate.OneOf([status.value for status in TaskStatus]))
