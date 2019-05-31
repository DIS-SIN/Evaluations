from .base_schema import schema
from marshmallow.fields import Nested
from src.models.survey_model import SurveyModel

class SurveySchema(schema.ModelSchema):
   questions = Nested('QuestionSchema', many = True, exclude = ('survey',))
   class Meta:
        model = SurveyModel

