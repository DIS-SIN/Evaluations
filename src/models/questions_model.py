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
    addedOn = base.Column(base.DateTime, server_default = func.now())
    updatedOn = base.Column(base.DateTime, server_default=func.now(), onupdate=func.now())
    questionKey = base.Column(base.Text)
    surveyId = base.Column(
        base.Integer,
        ForeignKey(
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
        ForeignKey(
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
        ForeignKey(
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

    def set_prefix(self, prefix):
        self.prefix = prefix

    def set_questionKey(self):
        if hasattr(self, "prefix"):
            self.questionKey = f"{self.prefix}_sid_{self.id}"
        else:
            self.questionKey = f"{self.type.type}_qid_{self.id}"
            print(self.questionKey)
    
    def set_item_order(self, order, item):
        if not hasattr(self, "order_registry"):
            self.create_order_registry()
        else:
            self.recount_active()
        if (self.type is not None and (self.type.type == "matrix" or self.type.type == "ranking")):
            if self.item_count == 0:
                raise ValueError(
                    "There are currently no subQuestions in this question " +
                    "please add a subQuestion before setting the order"
                )
            elif order < 1 or order > self.item_count:
                raise IndexError(
                    "You have specified an order which is out of bound " +
                    "from the index of 1 to " + str(self.item_count)
             )

            if not (hasattr(self, "order") and hasattr(self, "randomize")):
                raise AttributeError(
                    "item passed into this function must have " +
                    "an order and randomize property")
            elif not item in self.subQuestions:
                raise ValueError(
                    f"The subQuestion {item} is not in the subQuestions relationship"
                )
            
            if item.status != "active":
                raise ValueError(
                    "subQuestion must be active in order to set the order"
                )
            elif self.order_registry.get(item.order) is not None:
                raise ValueError(
                    f"An item in this section already exists in order {order}"
                )
            else:
                item.order = order
                item.randomize = False
                self.order_registry[order] = item
        else:
            raise ValueError("The question must have type ranking or matrix in order to be able to set the order for sub questions")
        
        def create_order_registry(self):
            self.order_registry = {}
            self.item_count = 0
            for sub in self.subQuestions:
                if sub.status == "active":
                    self.item_count += 1
                    if sub.order is not None:
                        self.order_registry[sub.order] = sub
        
        def recount_active(self):
            self.item_count = 0
            for sub in self.subQuestions:
                if sub.status == "active":
                    self.item_count += 1
                        







