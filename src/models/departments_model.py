
from .base_model import base

class DepartmentModel(base.Model):
    __tablename__ = "departments_refrence"
    id = base.Column(base.Integer, primary_key =True)
    language = base.Column(base.Text, nullable = False)
    department = base.Column(base.Text, nullable = False)
    abbreviation = base.Column(base.Text)

