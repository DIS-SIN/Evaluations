from flask import Flask

def init_load_schemas():
    from .question_loader_schema import QuestionLoaderSchema
    from .section_loader_schema import SectionLoaderSchema
    from .survey_loader_schema import SurveyLoaderSchema
