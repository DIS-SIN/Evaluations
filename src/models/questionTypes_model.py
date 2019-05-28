from .base_model import base
from sqlalchemy.sql import func

class QuestionTypeModel(base.Model):
    __tablename__ = "question_types"
    id = base.Column(base.Integer, primary_key = True)
    type = base.Column(base.Text, nullable = False)
    addedOn = base.Column(base.DateTime(timezone = True), server_default = func.now())
