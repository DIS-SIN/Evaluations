from .base_model import base

class RegionModel(base.Model):
    __tablename__ = "regions_refrence"
    id = base.Column(base.Integer, primary_key = True)
    language = base.Column(base.Text, nullable = False)
    region = base.Column(base.Text, nullable = False)
