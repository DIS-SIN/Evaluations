from src.models.regions_model import RegionModel
from .base_schema import schema

class RegionSchema(schema.ModelSchema):
    class Meta:
        model = RegionModel
   
