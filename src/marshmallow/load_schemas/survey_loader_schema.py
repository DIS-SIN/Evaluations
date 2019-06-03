from marshmallow import Schema, post_load, ValidationError, validates, validates_schema
from marshmallow.fields import Nested, String, Integer, Nested
from src.database import get_db
from src.models.survey_model import SurveyModel

class SurveyLoaderSchema(Schema):
    title = String(required=True)
    description = String(required=True)
    language = String(required=True)
    questions = Nested("QuestionLoaderSchema", many=True)

    @validates("language")
    def validate_language_options(self, value):
        if value != "en" and value != "fr":
            raise ValidationError(
                f"language must be either en or fr: {value} is not supported"
            )
    
    @validates_schema
    def validate_schema(self, data):
        questions =  data.get("questions")
        print(questions)
        if questions is None or questions == []:
            raise ValidationError(
                "at least one question is needed to create a survey",
                "questions"
            )
    
    @post_load
    def make_survey(self, data):
        session = get_db()
        survey = SurveyModel(session = session)
        survey.title = data['title']
        survey.description = data['description']
        survey.language = data['language']
        for question in data["questions"]:
            survey.questions.append(question)
        return survey





