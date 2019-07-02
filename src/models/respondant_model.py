from .base_model import base
import hashlib
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func
from src.utils.slug_generator import generate_slug

class RespondantModel(base.Model):
    __tablename__ = "respondants"
    id = base.Column(base.Integer, primary_key = True)
    addedOn = base.Column(base.DateTime, server_default = func.now())
    slug = base.Column(base.Text, nullable = False, unique = True)
    respondantHash = base.Column(base.Text, nullable = False, unique = True)
    departmentId = base.Column(
        base.Integer, 
        base.ForeignKey(
            'departments_reference.id', 
             ondelete="SET NULL", 
             onupdate="CASCADE"
            )
        )
    regionId = base.Column(
        base.Integer,
        base.ForeignKey(
            'regions_reference.id',
            ondelete="SET NULL",
            onupdate="CASCADE"
        )
    )
    classificationId = base.Column(
        base.Integer,
        base.ForeignKey(
            'classifications_reference.id',
            ondelete="SET NULL",
            onupdate="CASCADE"
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
    
    def set_survey_hash(self, session = None):
        if self.slug is None:
            if self.session is None:
                raise ValueError("session is required to initialise slug which feeds the hash")
            else:
                self.set_slug(session)

        hash_datetime = self.addedOn or datetime.utcnow()
        hash_datetime = bytes(str(hash_datetime), encoding = "utf-8")

        hash = hashlib.sha1()
        hash.update(hash_datetime)
        hash.update(self.slug)
        self.respondantHash = hash.hexdigest()
 




