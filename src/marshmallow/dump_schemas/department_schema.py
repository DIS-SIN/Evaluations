from .base_schema import schema
from src.models.departments_model import DepartmentModel
from src.models.base_model import base
from marshmallow import post_load, ValidationError

class DepartmentSchema(schema.ModelSchema):
    class Meta:
        model = DepartmentModel
    