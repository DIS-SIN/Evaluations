from .base_model import base
from sqlalchemy.dialects.postgresql import JSONB

class SurveySchemalessModel(base.Model):
    __tablename__="survey_schemaless"
    id = base.Column(base.Integer, primary_key = True)
    survey = base.Column(JSONB, nullable = False)