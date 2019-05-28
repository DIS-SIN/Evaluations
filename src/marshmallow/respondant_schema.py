
from .base_schema import schema
from marshmallow.fields import Nested
from src.models.respondant_model import RespondantModel
from src.models.classification_model import ClassificationModel
from src.models.departments_model import DepartmentModel
from src.models.regions_model import RegionModel
from marshmallow import pre_load, validates_schema, ValidationError
from src.models.base_model import base

class RespondantSchema(schema.ModelSchema):
    classification = Nested('ClassificationSchema', exclude = ('addedOn', 'respondants', 'id'))
    region = Nested('RegionSchema', exclude = ('addedOn', 'respondants', 'id'))
    department = Nested('DepartmentSchema', exclude = ('addedOn', 'respondants', 'id'))
    class Meta:
        model = RespondantModel
    
    
    
        
        
        


    
    