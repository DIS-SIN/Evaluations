
from .base_model import base
from sqlalchemy.sql import func


class ConductedSurveyStatusModel(base.Model):
    __tablename__ = "conducted_survey_status_refrence"
    id = base.Column(base.Integer, primary_key = True)
    status = base.Column(base.Text, nullable = False)
    description = base.Column(base.Text)
    addedOn = base.Column(base.DateTime, server_default= func.now())