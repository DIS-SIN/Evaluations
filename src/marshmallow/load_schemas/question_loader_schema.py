from marshmallow import Schema, post_load, validates_schema, ValidationError
from marshmallow.fields import String, Integer, Dict, Nested
from src.database import get_db
from src.models.questions_model import QuestionModel

class QuestionLoaderSchema(Schema):
    order = Integer()
    question = String(required=True)
    options = Dict()
    questionType = Nested(
        "QuestionTypeLoaderSchema"
    ),
    typeId = Integer()

    @validates_schema
    def validate_schema(self, data):
        typeId = data.get("typeId")
        type = data.get("questionType")
        if type is not None and typeId is not None:
            raise ValidationError(
                "you may only enter one of type or typeId both cannot be present",
                "typeId",
                "type"
            )

    @post_load
    def load_question(self, data):
        session = get_db()
        question =  QuestionModel()

        if data.get("order") is not None:
            question.order = data["order"]
        
        if data.get("typeId") is not None:
            question.typeId = data["type"]
        elif data.get("type") is not None:
            question.questionType = data.get("questionType")
        
        if data.get("options") is not None:
            question.options = data['options']
        
        question.question = data['question']
        
        return question
        

        





        

