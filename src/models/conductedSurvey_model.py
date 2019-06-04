from  .base_model import base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from src.utils.slug_generator import generate_slug
import src.models.status_model as stm
import hashlib
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class ConductedSurveyModel(base.Model):
    __tablename__ = "conducted_surveys"
    id = base.Column(base.Integer, primary_key = True)
    addedOn = base.Column(base.DateTime, server_default = func.now())
    questions = association_proxy("conductedSurveyModelQuestions", 'question')
    slug = base.Column(base.Text, nullable = False, unique = True)
    surveyHash = base.Column(base.Text, nullable = False, unique = True)
    statusId = base.Column(base.Integer, base.ForeignKey(
        'status_refrence.id',
         ondelete = "SET NULL",
         onupdate = "CASCADE"
    ))
    status = relationship(
        'StatusModel',
        backref= "conductedSurveys"
    )
    respondantId = base.Column(
        base.Integer,
        base.ForeignKey(
           'respondants.id',
            ondelete = "CASCADE",
            onupdate = "CASCADE"
        )
    )
    respondant = relationship(
       'RespondantModel',
        backref= backref(
            'conductedSurveys',
            passive_deletes = True,
            cascade = "all, delete-orphan"
        )
    )
    surveyId = base.Column(
        base.Integer,
        base.ForeignKey(
            'surveys.id',
            ondelete = "CASCADE",
            onupdate = "CASCADE"
        )
    )
    survey = relationship(
        'SurveyModel',
        back_populates = "conductedSurveys"

    )
    sentimentScore = base.Column(base.Float(2))
    magnitudeScore = base.Column(base.Float(2))

    
    def __init__(self, session = None, *args, **kwargs):
        if session is not None:
            self.set_slug(session)
            self.set_status(session)
        super(ConductedSurveyModel, self).__init__(*args, **kwargs)
    def set_slug(self, session):
        self.slug = generate_slug('conductedSurvey', ConductedSurveyModel, session)
    def set_status(self, session):
        self.status = session.query(stm.StatusModel).filter_by(
            status="active"
        ).one()
    def set_survey_hash(self, session = None):
        if self.slug is None:
            if self.session is None:
                raise ValueError("session is required to initialise slug which feeds the hash")
            else:
                self.set_slug(session)

        hash_datetime = self.addedOn or datetime.utcnow()
        hash_datetime = bytes(str(hash_datetime), encoding = "utf-8")

        hash = hashlib.sha1()
        hash.update(hash_datetime)
        hash.update(self.slug)
        self.surveyHash = hash.hexdigest()


class ConductedSurveyModelQuestions(base.Model):
    __tablename__= "conducted_survey_questions"
    id = base.Column(base.Integer, primary_key = True)
    conductedSurveyId = base.Column(
        base.Integer,
        base.ForeignKey(
            'conducted_surveys.id',
            ondelete = "CASCADE",
            onupdate = "CASCADE"
            )
        )
    questionId = base.Column(
        base.Integer,
        base.ForeignKey(
           'questions.id',
           ondelete = "CASCADE",
           onupdate = "CASCADE"
        )
    )
    
    addedOn = base.Column(base.DateTime, server_default = func.now())
    conductedSurvey = relationship(
        'ConductedSurveyModel',
         backref= backref(
            'conductedSurveyModelQuestions',
            passive_deletes = True,
            cascade = "all, delete-orphan"
        )
    )
    question = relationship(
        'QuestionModel',
        backref= backref(
            'conductedSurveyModelQuestions',
             passive_deletes = True,
             cascade = "all, delete-orphan"
        )
    )

    def __init__(self, conductedSurvey = None, question= None, *args, **kwargs):
        super(ConductedSurveyModelQuestions, self).__init__(*args, **kwargs)
        if isinstance(conductedSurvey, ConductedSurveyModel):
            self.conductedSurvey = conductedSurvey
            self.question = question
        else:
            self.question = conductedSurvey
            self.conductedSurvey = question
    


