from flask import Flask
from src.database import get_db
from src.models.conductedSurveyStatus_model import ConductedSurveyStatusModel
from src.models.surveyStatus_model import SurveyStatusModel

def load_statuses(app: Flask):
    with app.app_context():
       load_conductedSurveyStatuses()
       load_surveyStatuses()

def load_conductedSurveyStatuses():
    session = get_db()

    active = ConductedSurveyStatusModel(
        status="active",
        description = "The conducted survey is currently being conducted"
    )
    closed = ConductedSurveyStatusModel(
        status="closed",
        description = "The conducted survey is currently closed for answering or modification"
    )
    processing = ConductedSurveyStatusModel(
        status = "processing",
        description = "The survey data is being processed by the server"
    )
    released = ConductedSurveyStatusModel(
        status = "released",
        description = "The survey data has been processed and is now available through the api "
    )

    session.add(active)
    session.add(closed)
    session.add(processing)
    session.add(released)

    session.commit()

def load_surveyStatuses():
    session = get_db()

    draft = SurveyStatusModel(
        status = "draft",
        description = "The survey is in draft mode and not released"
    )

    editing = SurveyStatusModel(
        status = "editing",
        description = "The survey is currently being edited"
    )

    released = SurveyStatusModel(
        status = "released",
        description = "The survey has finished being edited and can be released"
    )

    session.add(draft)
    session.add(editing)
    session.add(released)

    session.commit()


