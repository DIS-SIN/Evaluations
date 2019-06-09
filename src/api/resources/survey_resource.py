from flask_restful import Resource
from src.models.survey_model import SurveyModel
from src.marshmallow.dump_schemas.survey_schema import SurveySchema
from src.marshmallow.load_schemas.survey_loader_schema import SurveyLoaderSchema
from src.database import get_db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from marshmallow import ValidationError
from flask import request
from src.api.utils.load_helpers import load_object
from src.api.utils.dump_helpers import get_one_row_by_id, get_one_row_by_slug, get_all_rows

class SurveyResource(Resource):
    def get(self, id = None, slug = None):
        session = get_db()
        if id is not None:
           """
           # query for active sections and questions
           survey = session.query(SurveyModel).\
                join(
                    and_(SurveyModel.questions, QuestionModel.status == "active"), isouter = True).\
                join(
                    and_(SurveyModel.sections, SectionModel.status == "active", isouter = True)
                ).\
                filter(
                    SurveyModel.id == data["id"]
                ).options(
                    contains_eager(SurveyModel.questions), contains_eager(SurveyModel.sections)
                ).\
                one_or_none()
           """
            dump, status = get_one_row_by_id(
                session,
                SurveyModel,
                id,
                SurveySchema
            )    
        elif slug is not None:
            dump, status = get_one_row_by_slug(
                session,
                SurveyModel,
                slug,
                SurveySchema
            )
        else:
            dump, status = get_all_rows(
                session,
                SurveyModel,
                SurveySchema
            )
        return dump, status
    
    def post(self):
        json = request.get_json()
        value, status = load_object(SurveyLoaderSchema(), json)
        return value, status




            


        



