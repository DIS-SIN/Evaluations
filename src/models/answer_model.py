from .base_model import base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

class AnswerModel(base.Model):
    __tablename__="answers"
    id = base.Column(base.Integer, primary_key = True)
    answer = base.Column(base.Text)
    addedOn = base.Column(base.DateTime, server_default = func.now())
    updateOn = base.Column(
        base.DateTime,
        server_default = func.now(),
        onupdate = func)
    sentimentScore = base.Column(base.Float(3))
    magnitudeScore = base.Column(base.Float(3))
    conductedSurveyQuestionId = base.Column(
        base.Integer,
        base.ForeignKey(
            'conducted_survey_questions.id',
            ondelete = "CASCADE",
            onupdate = "CASCADE"
        )
    )
    conductedSurveyQuestion = relationship(
        'ConductedSurveyModelQuestions',
        backref=backref(
            "answer",
            uselist = False
        ),
        uselist= False
    )
    