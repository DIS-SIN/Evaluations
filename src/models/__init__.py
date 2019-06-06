from flask import Flask


def init_models(app: Flask) -> None:
    from .base_model import base
    base.init_app(app)

    from .classification_model import ClassificationModel
    from .regions_model import RegionModel
    from .departments_model import DepartmentModel
    from .respondant_model import RespondantModel

    from .answer_model import AnswerModel
    from .questions_model import QuestionModel
    from .questionTypes_model import QuestionTypeModel
    from .survey_model import SurveyModel
    
    from .sectionType_model import SectionTypeModel
    from .section_model import SectionModel

    from .conductedSurveyStatus_model import ConductedSurveyStatusModel
    from .surveyStatus_model import SurveyStatusModel
    from .conductedSurvey_model import ConductedSurveyModel, ConductedSurveyModelQuestions
    from .surveySchemaless_model import SurveySchemalessModel
