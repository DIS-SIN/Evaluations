from flask_restful import Resource
from src.models.survey_model import SurveyModel
from src.marshmallow.survey_schema import SurveySchema
from src.database import get_db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from marshmallow import ValidationError
from src.models.conductedSurvey_model import ConductedSurveyModel
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
            


        



