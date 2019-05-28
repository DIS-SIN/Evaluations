from .base_model import base

from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func

class RespondantModel(base.Model):
    __tablename__ = "respondants"
    id = base.Column(base.Integer, primary_key = True)
    classification = base.Column(base.Text, nullable = False)
    addedOn = base.Column(base.DateTime(timezone = True), server_default = func.now())
    departmentId = base.Column(
        base.Integer, 
        base.ForeignKey(
            'departments_refrence.id', 
             ondelete = "SET NULL", 
             onupdate="CASCADE"
            )
        )
    regionId = base.Column(
        base.Integer,
        base.ForeignKey(
            'regions_refrence.id',
            ondelete =  "SET NULL",
            onupdate = "CASCADE"
        )
    )
    classificationId = base.Column(
        base.Integer,
        base.ForeignKey(
            'classifications_refrence.id',
            ondelete = "SET NULL",
            onupdate = "CASCADE"
        )
    )
    department = relationship(
        "DepartmentModel", 
        backref = backref(
           'respondants', 
            passive_deletes = True
        ),
        uselist= False
    )
    classification = relationship(
        "ClassificationModel", 
        backref = backref(
           'respondants', 
            passive_deletes = True
        ),
        uselist= False
    )
    region = relationship(
        "RegionModel", 
        backref = backref(
           'respondants', 
            passive_deletes = True
        ),
        uselist= False
    )



