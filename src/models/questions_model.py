from .base_model import base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func

class QuestionModel(base.Model):
    __tablename__ = "questions"
    id = base.Column(base.Integer, primary_key = True)
    order = base.Column(base.Integer)
    randomize = base.Column(base.Boolean, default = True)
    question = base.Column(base.Text, nullable = False)
    options = base.Column(JSONB)
    addedOn = base.Column(base.DateTime(timezone = True), server_default = func.now())
    questionKey = base.Column(base.Text, nullable = False)
    
    surveyId = base.Column(base.Integer,
                           base.ForeignKey(
                               'surveys.id',
                                ondelete = "CASCADE",
                                onupdate = "CASCADE"
                           )
                        )
    survey = relationship(
        'SurveyModel',
        back_populates = "questions"
    )

    sectionId = base.Column(
        base.Integer,
        base.ForeignKey(
            "sections.id",
            ondelete="CASCADE",
            onupdate="CASCADE"
        )
    )
    sections = relationship(
        "SectionModel",
        back_populates="questions"
    )

    typeId = base.Column(
        base.Integer,
        base.ForeignKey(
            'question_types.id',
            ondelete = "SET NULL",
            onupdate = "CASCADE"
        )
    )
    questionType = relationship(
        "QuestionTypeModel",
        backref="questions"
    )

    conductedSurveys = association_proxy('conductedSurveyQuestions', 'conductedSurvey')



