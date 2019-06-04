from .base_model import base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

class PreQuestionModel(base.Model):
    __tablename__ = "prequestions"
    id = base.column(base.Integer, primary_key = True)
    title = base.Column(base.Text)
    body = base.Column(base.Text, nullable = False)
    order = base.Column(base.Integer)
    randomize = base.Column(base.Boolean, default = False)
    addedOn = base.Column(base.DateTime, server_default= func.now())
    updatedOn = base.Column(base.DateTime, server_default=func.now())
    surveyId = base.Column(
        base.Integer,
        ForeignKey(
            "surveys.id",
            ondelete="CASCADE",
            onupdate="CASCADE"
        )
    )
    survey = relationship(
        "SurveyModel",
        back_populates="preQuestions",
    )

    questions = relationship(
        "QuestionModel",
        back_populates="preQuestions",
        cascade="all, delete-orphan"
    )

    def set_order(self, order):
        if self.survey is None:
            raise ValueError("PreQuestion has not yet been added to a survey. This must happen before assigning an order")
        else:
            self.survey.set_item_order(order, prequestion = self)
