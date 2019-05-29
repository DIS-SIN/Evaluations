from flask_restful import Resource
from src.models.survey_model import SurveyModel
from src.marshmallow.survey_schema import SurveySchema
from src.database import get_db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from marshmallow import ValidationError
from src.models.conductedSurvey_model import ConductedSurveyModel
from src.models.status_model import StatusModel
from src.models.answer_model import AnswerModel
from src.marshmallow.conductedSurvey_schema import ConductedSurveySchema
from flask import request
class SurveyResource(Resource):
    def get(self, id = None, slug = None):
        session = get_db()
        if id is not None:
            try:
                survey = session.query(SurveyModel).filter_by(id=id).one()
            except NoResultFound:
                return {
                    "error": f"No results could be found for id: {id}" 
                }, 400
            except Exception as e:
                return {
                    "error": f"An internal error has occured: {repr(e)}"
                }, 500
            try:
                survey_dump = SurveySchema().dump(survey)
                if bool(survey_dump.errors) is False:
                    return survey_dump.data, 200
                else: 
                    raise ValidationError(survey_dump.errors) 
            except ValidationError as e:
                return {
                    "error" : f"An internal error has occured: {repr(e)}"
                }
        elif slug is not None:
            try:
                survey = session.query(SurveyModel).filter_by(slug = slug).one()
            except NoResultFound:
                return {
                    "error": f"No results could be found for id: {slug}" 
                }, 400
            except Exception as e:
                return {
                    "error": f"An internal error has occured: {repr(e)}"
                }, 500
            try:
                survey_dump = SurveySchema().dump(survey)
                if bool(survey_dump.errors) is False:
                    return survey_dump.data, 200
                else: 
                    raise ValidationError(survey_dump.errors) 
            except ValidationError as e:
                return {
                    "error" : f"An internal error has occured: {repr(e)}"
                }
        else:
            dumped_surveys = []
            all_surveys = session.query(SurveyModel)
            for survey in all_surveys:
                dumped_surveys.append(SurveySchema().dump(survey).data)
            return dumped_surveys, 200
        return {}, 200
    def post(self):
        json = request.get_json()
        session = get_db()
        if json is None:
            return {
                'error': "JSON not submitted"
            }, 400
        if json.get("conductedSurveyId") is None:
            return {
                "error": "Must submit ConductedSurveyId"
            }, 400
        else:
            conducted_survey = session.query(ConductedSurveyModel).filter_by(
                id = json.get("conductedSurveyId")
            ).one_or_none()
            if conducted_survey is None:
                return {
                    "error": "No conducted survey with id " + json.get("conductedSurveyId")
                }, 400
        
        if json.get("questions") is None:
            return {
                "error": "questions cannot be none"
            }
        else:
            questions_registry  = {}
            for question in conducted_survey.conductedSurveyModelQuestions:
                questions_registry[question.questionId] = question

            for question in json.get("questions"):
                id = question.get("questionId")
                if  id is None:
                    return {
                        "error": "Must provide question id for all questions"
                    }
                elif questions_registry.get(id) is None:
                    return {
                        "error": f"questionId {id} does not exist in this conducted survey"
                    }
                answer = question.get("answer")
                question = questions_registry.get(id)
                if question.answer is None:
                    answer_row = AnswerModel(
                       answer = answer
                    )
                    print(answer_row)

                    question.answer = answer_row
                else:
                    question.answer.answer = answer
            
            closed = session.query(StatusModel).filter_by(
                status = "closed"
            ).one()
            conducted_survey.status = closed
            session.commit()
            conducted_survey_dump = ConductedSurveySchema().dump(conducted_survey).data
            return conducted_survey_dump, 200




            


        



