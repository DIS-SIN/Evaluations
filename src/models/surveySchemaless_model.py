from .base_model import base
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

class SurveySchemalessModel(base.Model):
    __tablename__="survey_schemaless"
    id = base.Column(base.Integer, primary_key = True)
    survey = base.Column(JSONB, nullable = False)
    addedOn = base.Column(base.DateTime, server_default = func.now())
    updatedOn = base.Column(
        base.DateTime,
        server_default = func.now(),
        onupdate = func.now()
    )
    conductedSurveyId = base.Column(
        base.Integer, ForeignKey(
            "conducted_surveys.id",
            ondelete="CASCADE",
            onupdate="CASCADE"
        )
    )