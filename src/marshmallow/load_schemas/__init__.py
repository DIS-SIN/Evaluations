from flask import Flask

def init_load_schemas():
    from .question_loader_schema import QuestionLoaderSchema
    from .survey_loader_schema import SurveyLoaderSchema
