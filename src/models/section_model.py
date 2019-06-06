from .base_model import base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.sql import func

class SectionModel(base.Model):
    __tablename__ = "sections"
    id = base.Column(base.Integer, primary_key = True)
    title = base.Column(base.Text)
    body = base.Column(base.Text)
    order = base.Column(base.Integer)
    randomize = base.Column(base.Boolean, default = True)
    questionIndex = base.Column(JSONB)
    addedOn = base.Column(base.DateTime, server_default= func.now())
    updatedOn = base.Column(base.DateTime, server_default=func.now())

    typeId = base.Column(base.Integer, ForeignKey(
        "section_types.id",
        ondelete= "SET NULL",
        onupdate= "CASCADE"
    ))
    type = relationship(
        "SectionTypeModel"
    )
    parentId = base.Column(base.Integer, ForeignKey(
        "sections.id",
        ondelete="CASCADE",
        onupdate="CASCADE"
      )
    )
    subsections = relationship(
        "SectionModel",
        passive_deletes = True,
        cascade="all, delete-orphan"
    )

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
        back_populates="sections",
    )

    questions = relationship(
        "QuestionModel",
        back_populates="sections",
        cascade="all, delete-orphan"
    )

    def set_order(self, order):
        if self.survey is None:
            raise ValueError("PreQuestion has not yet been added to a survey. This must happen before assigning an order")
        else:
            self.survey.set_item_order(order, self)
    
    def set_item_order(self, order, item):
        if bool(self.order_registry) is False:
            self.order_registry = {}
            self.item_count = 0
            for question in self.questions:
                if question.order is not None:
                    self.order_registry[question.order] = question 
                self.item_count += 1
            
            for section in self.subsections:
                if section.order is not None:
                    self.order_registry[section.order] = section
                self.item_count += 1 

        if self.item_count == 0:
            raise IndexError(
                "There are currently no items in this section please add an item before setting an order"
            )
        elif order < 1 or order > self.item_count:
            raise IndexError(
                "You have specified an order which is out of bound from the index of 1 to " + str(self.item_count)
            )
        
        if not (hasattr(item, "order") and hasattr(item, "randomize")):
            raise AttributeError("item passed into this function must have an order and randomize property")
        
        if self.order_registry.get(item.order) is not None:
            raise ValueError(
                f"An item in this section already exists in order {order}"
            )
        else:
            item.order = order
            item.randomize = False
            self.order_registry[order] = item
            self.item_count += 1

        
        
