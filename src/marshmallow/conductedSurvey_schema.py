from .base_schema import schema
from src.models.conductedSurvey_model import ConductedSurveyModel, ConductedSurveyModelQuestions
from marshmallow.fields import Nested

class ConductedSurveyModelQuestionsSchema(schema.ModelSchema):
    question = Nested('QuestionSchema', exclude = ('survey', 'conductedSurveys'))
    answer = Nested('AnswerSchema', exclude = ('conductedSurveyQuestion'))
    class Meta:
        model = ConductedSurveyModelQuestions

class ConductedSurveySchema(schema.ModelSchema):
    questions = Nested(
        'ConductedSurveyModelQuestionsSchema',
        attribute = "conductedSurveyModelQuestions",
        exclude = ('conductedSurvey',),
        many = True)
    class Meta:
        model = ConductedSurveyModel