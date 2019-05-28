from src.models.classification_model import ClassificationModel
from .base_schema import schema
from marshmallow import post_load, ValidationError
from src.models.base_model import base

class ClassificationSchema(schema.ModelSchema):
    class Meta:
        model = ClassificationModel
    
        
        

