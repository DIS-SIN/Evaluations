
from .base_model import base


class StatusModel(base.Model):
    __tablename__ = "status_refrence"
    id = base.Column(base.Integer, primary_key = True)
    status = base.Column(base.Text, nullable = False)
    category = base.Column(base.Text, nullable = False)