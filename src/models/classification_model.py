
from .base_model import base

class ClassificationModel(base.Model):
    __tablename__ = "classifications_refrence"
    id = base.Column(base.Integer, primary_key =True)
    classification = base.Column(base.Text, nullable = False)