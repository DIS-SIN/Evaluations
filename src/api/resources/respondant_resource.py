from flask_restful import Resource
from flask import request
from src.models.respondant_model import RespondantModel
from src.marshmallow.respondant_schema import RespondantSchema
from src.database import get_db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from marshmallow import ValidationError
from src.models.departments_model import DepartmentModel
from src.models.regions_model import RegionModel
from src.models.classification_model import ClassificationModel
from src.models.survey_model import SurveyModel
from src.models.conductedSurvey_model import ConductedSurveyModel

class RespondantResource(Resource):
    
    def get(self, id= None, slug = None):
        session = get_db()
        if id is not None:
            try:
                respondant = session.query(RespondantModel).filter_by(id=id).one() 
            except NoResultFound:
                return {
                    "error": f"No results could be found for id: {id}" 
                }, 400
            except Exception as e:
                return {
                    "error": f"An internal error has occured: {repr(e)}"
                }, 500
            try:
                respondant_dump = RespondantSchema().dump(respondant)
                if bool(respondant_dump.errors) is False:
                    return respondant_dump.data, 200
                else: 
                    raise ValidationError(respondant_dump.errors) 
            except ValidationError as e:
                return {
                    "error" : f"An internal error has occured: {repr(e)}"
                }
        elif slug is not None:
            try:
                respondant = session.query(RespondantModel).filter_by(slug = slug).one()
            except NoResultFound:
                return {
                    "error": f"No results could be found for id: {slug}" 
                }, 400
            except Exception as e:
                return {
                    "error": f"An internal error has occured: {repr(e)}"
                }, 500
            try:
                respondant_dump = RespondantSchema().dump(respondant)
                if bool(respondant_dump.errors) is False:
                    return respondant_dump.data, 200
                else: 
                    raise ValidationError(respondant_dump.errors) 
            except ValidationError as e:
                return {
                    "error" : f"An internal error has occured: {repr(e)}"
                }
        else:
            dumped_respondants = []
            all_respondants = session.query(RespondantModel)
            for respondant in all_respondants:
                dumped_respondants.append(RespondantSchema().dump(respondant).data)
            return dumped_respondants, 200
        return {}, 200

    def post(self):
        session = get_db()
        json = request.get_json()
        if json is None:
            return {
                'error': 'No JSON was posted'
            }
        if json.get('surveyId') is None:
            if json.get('surveySlug') is None:
                return {
                    'error': 'either surveyId or surveySlug must be provided'
                }, 400
            else:
                survey = session.query(SurveyModel).filter_by(
                    slug = slug
                ).one_or_none()
                if survey is None:
                    return {
                        'error': f"survey does not exist with slug " + json.get("surveySlug")
                    }, 400
        else:
            survey = session.query(SurveyModel).filter_by(
                id = json.get("surveyId")
            ).one_or_none()
            if survey is None:
                return {
                    'error': f"survey does not exist with id " + json.get("surveyId")
                }

        if json.get('department') is None or json.get('department') == '':
            return {
                'error': 'department must not be None or Empty'
            }
        else:
            department = session.query(DepartmentModel).filter_by(
                department = json.get('department')
            ).one_or_none()
            if department is None:
                return {
                    'error': f"department {json.get('department')} does not exist"
                }, 400
        if json.get('region') is None or json.get('region') == '':
            return {
                'error': 'region must not be None or Empty'
            }, 400
        else:
            region = session.query(RegionModel).filter_by(
                region = json.get('region')
            ).one_or_none()
            if region is None:
                return {
                    'error': f"region {json.get('region')} does not exist"
                }
        if json.get('classification') is None or json.get('classification') == '':
            return {
                'error': 'classification must not be None or Empty'
            }, 400
        else:
            classification = session.query(ClassificationModel).filter_by(
                classification = json.get('classification')
            ).one_or_none()
            if classification is None:
                return {
                    'error': f"classification {json.get('classification')} does not exist"
                }, 400
        
        respondant = RespondantModel(
            session= session,
            classification = classification,
            department = department,
            region = region
        )
        try:
            session.add(respondant)
            session.commit()
        except Exception as e:
            return {
                'error': f"An internal error has occured {repr(e)}"
            }, 500 

        conducted_survey_model = survey.create_conducted_survey(
            respondant,
            session
        )
        session.add(conducted_survey_model)
        session.commit()

        return {}, 200 
       

        


