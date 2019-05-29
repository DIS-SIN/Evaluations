from .base_schema import schema
from marshmallow.fields import Nested
from src.models.answer_model import AnswerModel

class AnswerSchema(schema.ModelSchema):
    class Meta:
        model = AnswerModel