from .base_model import base

from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func
from src.utils.slug_generator import generate_slug

class RespondantModel(base.Model):
    __tablename__ = "respondants"
    id = base.Column(base.Integer, primary_key = True)
    classification = base.Column(base.Text, nullable = False)
    addedOn = base.Column(base.DateTime, server_default = func.now())
    slug = base.Column(base.Text, nullable = False, unique = True)
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
    def __init__(self, session = None, *args, **kwargs):
        if session is not None:
            self.set_slug(session)
        super(RespondantModel, self).__init__(*args, **kwargs)
    def set_slug(self, session):
        self.slug = generate_slug('respondant', RespondantModel, session)
 




