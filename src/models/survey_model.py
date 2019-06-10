from sqlalchemy.orm import relationship, backref
from .base_model import base
from src.utils.slug_generator import generate_slug
import src.models.conductedSurvey_model as csm
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ForeignKey

class SurveyModel(base.Model):
    __tablename__ = "surveys"
    id = base.Column(
        base.Integer,
        primary_key = True
    )
    slug = base.Column(base.Text, nullable = False, unique = True)
    questionsIndex = base.Column(JSONB)
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

    statusId = base.Column(
        base.Integer,
        ForeignKey(
            "survey_status_refrence.id",
            ondelete= "SET NULL",
            onupdate="CASCADE"
        )
    )
    status = relationship(
        "SurveyStatusModel"
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

    sections = relationship(
        "SectionModel",
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
    
    def set_item_order(self, order, item):
        if not hasattr(self, "order_registry"):
            self.order_registry = {}
            self.item_count = 0
            for section in self.sections:
                if section.status == "active":
                    self.item_count += 1
                    if section.order is not None:
                         self.order_registry[prequestion.order] = section

            for question in self.questions:
                if question.status == "active":
                    self.item_count += 1
                    if question.order is not None:
                        self.order_registry[question.order] = question
        
        if self.item_count == 0:
            raise IndexError(
                "There are currently no items in the survey" +
                "please add an item before setting an order"
            )
        elif order < 1 or order > self.item_count:
            raise IndexError(
                "You have specified an order which is out of bound " +
                "from the index of 1 to " + str(self.item_count)
            )
        
        if not (hasattr(item, "order") and hasattr(item, "randomize")):
            raise AttributeError(
                "item passed into this function must have " +
                "an order and randomize property")
        elif not item in self.subQuestions:
            raise ValueError(
                f"The item {item} is not in the questions "+
                "or the sections relationshop"
            )

        if item.status != "active":
            raise ValueError(
                "Item must be active in order to set the order"
            )
        elif self.order_registry.get(item.order) is not None:
            raise ValueError(
                f"An item in this survey already exists {order}"
            )
        else:
            item.order = order
            item.randomize = False
            self.order_registry[order] = item
            self.item_count += 1



    

        


