from .base_model import base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, CheckConstraint

class QuestionModel(base.Model):
    __tablename__ = "questions"
    id = base.Column(base.Integer, primary_key = True)
    order = base.Column(base.Integer)
    randomize = base.Column(base.Boolean, default = True)
    status = base.Column(
        base.Text,
        CheckConstraint("status = 'active' OR status = 'deactive'"),
        nullable = False,
        default = "active"
    )
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

    type = relationship(
        "QuestionTypeModel"
    )

    parentId = base.Column(
        base.Integer,
        ForeignKey(
            "questions.id",
            ondelete= "CASCADE",
            onupdate= "CASCADE"
        )
    )

    subQuestions = relationship(
        "QuestionModel",
        cascade= "all, delete-orphan"
    )

    conductedSurveys = association_proxy('conductedSurveyQuestions', 'conductedSurvey')

    def set_questionKey(self, prefix = None):
        if middle is not None:
            self.questionKey = f"{prefix}_sid_{self.id}"
        else:
            self.questionKey = f"{self.type.type}_qid_{self.id}"
    
    def set_item_order(self, order, item):
        
        if (
            question.type is not None 
            and (question.type.type == "matrix" or question.type.type == "ranking")
        ):
            if not hasattr(self, "order_registry"):
                self.order_registry = {}
                # complete order setting function for matrix-row and ranking-row questions 






