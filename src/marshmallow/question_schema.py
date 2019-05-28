from marshmallow.fields import Nested
from .base_schema  import schema
from src.models.questions_model import QuestionModel
class QuestionSchema(schema.ModelSchema):
    survey = Nested('SurveyModel', exclude = ('questions',))
    class Meta:
        model = QuestionModel
    