from marshmallow import Schema, post_load, validates_schema, ValidationError
from marshmallow.fields import String, Integer, Dict, Nested
from src.database import get_db
from src.models.questions_model import QuestionModel
from src.models.questionTypes_model import QuestionTypeModel

class QuestionLoaderSchema(Schema):
    id = Integer()
    order = Integer()
    question = String()
    options = Dict()
    type = String() 

    @validates_schema
    def validate_schema(self, data):
        if data.get("id") is not None:

            if data.get("question") is None:
                raise ValidationError(
                    "you must provide the text for the question to create the question"
                )

            if data.get("type") is None:
                raise ValidationError(
                    "you must provide the type of the question",
                    "type"
                )
                
    @post_load
    def load_question(self, data):
        session = get_db()
        if data.get("id") is not None:
            question = session.query(QuestionModel).filter_by(id=data["id"]).one_or_none()
            if question is None:
                raise ValidationError("The id for the question you have provided does not exist")
        else:
            question = QuestionModel(session = session)
    
        if data.get("type") is not None:
            type = session.query(QuestionTypeModel).filter_by(
                type=data['type']
            ).one_or_none()
            if type is None:
                raise ValidationError("The type " + data.get("type") + "is not supported")
            else:
                question.questionType = type
        
        if data.get("options") is not None:
            question.options = data["options"]
        
        deserialized_return = {
            "object":question
        }

        if data.get("order") is not None:
            deserialized_return['order'] = data['order']
        
        return deserialized_return





        





        

