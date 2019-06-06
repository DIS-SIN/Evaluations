from .base_model import base
from sqlalchemy.sql import func

class ClassificationModel(base.Model):
    __tablename__ = "classifications_refrence"
    id = base.Column(base.Integer, primary_key =True)
    classification = base.Column(base.Text, nullable = False)
    level = base.Column(base.Integer)
    addedOn = base.Column(base.DateTime, server_default = func.now())