from  .base_model import base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy


class ConductedSurveyModel(base.Model):
    __tablename__ = "conducted_surveys"
    id = base.Column(base.Integer, primary_key = True)
    addedOn = base.Column(base.DateTime(timezone = True), server_default = func.now())
    questions = association_proxy("conductedSurveyQuestions", 'question')
    statusId = base.Column(base.Integer, base.ForeignKey(
        'status_refrence.id',
         ondelete = "SET NULL",
         onupdate = "CASCADE"
    ))
    status = relationship(
        'StatusModel',
        backref= "conductedSurveys"
    )
    sentimentScore = base.Column(base.Float(2))
    magnitudeScore = base.Column(base.Float(2))

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
    addedOn = base.Column(base.DateTime(timezone = True), server_default = func.now())
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


