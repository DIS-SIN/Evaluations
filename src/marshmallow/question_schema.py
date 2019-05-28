from marshmallow.fields import Nested
from .base_schema  import schema
from src.models.questions_model import QuestionModel
from src.models.questionTypes_model import QuestionTypeModel
class QuestionSchema(schema.ModelSchema):
    survey = Nested('SurveyModel', exclude = ('questions',))
    questionType = Nested('QuestionTypeSchema', exclude = ('questions', 'addedOn'))
    class Meta:
        model = QuestionModel

class QuestionTypeSchema(schema.ModelSchema):
    class Meta:
        model = QuestionTypeModel