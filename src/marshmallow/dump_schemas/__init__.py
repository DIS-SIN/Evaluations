from flask import Flask
def init_dump_schemas(app: Flask):
    from .base_schema import schema
    schema.init_app(app)
    from .survey_schema import SurveySchema
    from .question_schema import QuestionSchema
    from .classification_schema import ClassificationSchema
    from .department_schema import DepartmentSchema
    from .regions_schema import RegionSchema
    from .respondant_schema import RespondantSchema
    from .answer_schema import AnswerSchema
    from .conductedSurvey_schema import (
        ConductedSurveySchema,
        ConductedSurveyModelQuestionsSchema
    )
    from .surveySchemaless_schema import SurveySchemalessSchema
