from .base_model import base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func

class QuestionModel(base.Model):
    __tablename__ = "questions"
    id = base.Column(base.Integer, primary_key = True)
    order = base.Column(base.Integer)
    question = base.Column(base.Text, nullable = False)
    options = base.Column(JSONB)
    addedOn = base.Column(base.DateTime(timezone = True), server_default = func.now())
    surveyId = base.Column(base.Integer,
                           base.ForeignKey(
                               'surveys.id',
                                ondelete = "CASCADE",
                                onupdate = "CASCADE"
                           )
                        )
    typeId = base.Column(
        base.Integer,
        base.ForeignKey(
            'question_types.id',
            ondelete = "SET NULL",
            onupdate = "CASCADE"
        )
    )
    survey = relationship(
        'SurveyModel',
        back_populates = "questions"
    )
    conductedSurveys = association_proxy('conductedSurveyQuestions', 'conductedSurvey')
    questionType = relationship(
        "QuestionTypeModel",
        backref="questions"
    )



