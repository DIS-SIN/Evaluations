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
    subQuestions = Nested("self", many=True)

    @validates_schema
    def validate_schema(self, data):
        if data.get("id") is not None:

            if data.get("question") is None:
                raise ValidationError(
                    "you must provide the text for the question to create the question",
                    "question"
                )

            if data.get("type") is None:
                raise ValidationError(
                    "you must provide the type of the question",
                    "type"
                )
            
            if (
                data.get("type") is not None 
                and (data["type"] == "matrix" or data["type"] == "ranking")
                and data.get("subQuestions") is None):
                raise ValidationError(
                    "you must provide at least one sub question for matrix and ranking type questions",
                    "subQuestions"
                )

                
    @post_load
    def load_question(self, data):
        session = get_db()
        if data.get("id") is not None:
            question = session.query(QuestionModel).filter_by(id=data["id"]).one_or_none()
            if question is None:
                raise ValidationError(
                    f"The id {data[id]} for the question you have provided does not exist",
                    "id"
                    )
        else:
            question = QuestionModel(session = session)
    
        if data.get("type") is not None:
            type = session.query(QuestionTypeModel).filter_by(
                type=data['type']
            ).one_or_none()
            if type is None:
                raise ValidationError("The type " + data.get("type") + "is not supported")
            else:
                question.type = type
        
        if data.get("options") is not None:
            question.options = data["options"]
        
        if data.get("subQuestions") is not None:
            if question.type.type != "matrix" and question.type.type != "ranking":
                raise ValidationError("Only matrix and ranking type questions may have sub questions")
            for sub in question.subQuestions:
                if sub not in data["subQuestions"]:
                    sub.status = "deactive"
            for sub in data['subQuestions']:
                if sub['object'] not in question.subQuestions:
                    question.subQuestions.append(sub['object'])
                elif sub.status == "deactive":
                    sub.status = "active"
            
            for sub in data['subQuestions']:
                if sub.get('order') is not None:
                    question.set_item_order(sub['order'], sub['object'])

            

        elif (
            question.type.type == "matrix" 
            or question.type.type == "ranking"
            ):
            for sub in question.subQuestions:
                if sub.status == "active":
                    sub.status == "deactive"
            question.status = "deactive"
        
        # handle the case of matrix and ranking questions
        # the sub questions of these types need the parent questionKey as a prefix
        if (question.questionKey is None and 
            question.type.type != "matrix-row" and 
            question.type.type != "ranking-row"):
            question.set_questionKey()
            if question.type.type == "matrix" or question.type.type == "ranking":
                for sub in question.subQuestions:
                    if sub.questionKey is None:
                        sub.set_questionKey(prefix= question.questionKey)


        deserialized_return = {
            "object":question
        }

        if data.get("order") is not None:
            deserialized_return['order'] = data['order']
        
        return deserialized_return





        





        

