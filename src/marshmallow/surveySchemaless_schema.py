from src.models.surveySchemaless_model import SurveySchemalessModel
from .base_schema import schema

class SurveySchemalessSchema(schema.ModelSchema):
    class Meta:
        model = SurveySchemalessModel