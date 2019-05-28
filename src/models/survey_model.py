from sqlalchemy.orm import relationship
from .base_model import base

class SurveyModel(base.Model):
    __tablename__ = "surveys"
    id = base.Column(
        base.Integer,
        primary_key = True
    )
    title = base.Column(
        base.Text,
        nullable = False
    )
    description = base.Column(
        base.Text
    )
    language = base.Column(
        base.Text
    )
    otherLanguageId = base.Column(
        base.Integer,
        base.ForeignKey(
            'surveys.id',
            ondelete = "SET NULL",
            onupdate = "CASCADE"
        )
    )
    otherLanguage = relationship(
        'SurveyModel',
        uselist= False
    )
    questions = relationship(
        'QuestionModel',
        back_populates="survey",
        cascade="all, delete-orphan"
    )