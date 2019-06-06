from .base_model import base
from sqlalchemy.sql import func

class RegionModel(base.Model):
    __tablename__ = "regions_refrence"
    id = base.Column(base.Integer, primary_key = True)
    language = base.Column(base.Text, nullable = False)
    region = base.Column(base.Text, nullable = False)
    addedOn = base.Column(base.DateTime, server_default = func.now())
