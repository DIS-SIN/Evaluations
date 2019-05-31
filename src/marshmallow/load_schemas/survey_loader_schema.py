from marshmallow import Schema, post_load
from marshmallow.fields import Nested, String, Integer

from src.models.survey_model import SurveyModel

class SurveyLoaderSchema(Schema):
    id = Integer()
    title = String(required=True)
    description = String()
    language = String()
    
    @post_load
    def make_survey(self, data):
        pass

