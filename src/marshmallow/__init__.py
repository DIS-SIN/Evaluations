from flask import Flask
def init_schemas(app: Flask):
    from .base_schema import schema
    schema.init_app(app)
    from .survey_schema import SurveySchema
    from .question_schema import QuestionSchema
