from sqlalchemy.orm import relationship
from .base_model import base
from src.utils.slug_generator import generate_slug
import src.models.conductedSurvey_model as csm
from sqlalchemy.sql import func

class SurveyModel(base.Model):
    __tablename__ = "surveys"
    id = base.Column(
        base.Integer,
        primary_key = True
    )
    slug = base.Column(base.Text, nullable = False, unique = True)
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
    addedOn = base.Column(
        base.DateTime,
        server_default = func.now(),
        onupdate = func.now()
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
    preQuestions = relationship(
        "PreQuestionModel",
        back_populates="survey",
        cascade="all, delete-orphan"
    )
    questions = relationship(
        'QuestionModel',
        back_populates="survey",
        cascade="all, delete-orphan"
    )
    conductedSurveys = relationship(
        'ConductedSurveyModel',
        back_populates="survey",
        passive_deletes = True,
        cascade="all, delete-orphan"
    )
    def __init__(self, session = None, *args, **kwargs):
        super(SurveyModel, self).__init__(*args,**kwargs)
        if session is not None:
            self.set_slug(session)


    def set_slug(self, session):
        self.slug = generate_slug('survey', SurveyModel, session)
    
    def create_conducted_survey(self, respondant, session):
        conducted_survey = csm.ConductedSurveyModel(session = session)
        conducted_survey.respondant = respondant
        for question in self.questions:
            conducted_survey.questions.append(question)
        self.conductedSurveys.append(conducted_survey)
        return conducted_survey
    

        


