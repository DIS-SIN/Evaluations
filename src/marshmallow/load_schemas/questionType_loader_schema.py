from marshmallow import Schema, post_load, ValidationError
from marshmallow.fields import String
from src.database import get_db
from src.models.questionTypes_model import QuestionTypeModel

class QuestionTypeLoaderSchema(Schema):
    type = String(required= True)

    @post_load
    def load_question_type(self, data):
        session = get_db()
        questionType = session.query(QuestionTypeModel).filter_by(
            type=data['type']
        ).one_or_none()
        if questionType is None:
            raise ValidationError(
                f"The Question Type {data['type']} you have specified does not exist"
            )
        else:
            return questionType




