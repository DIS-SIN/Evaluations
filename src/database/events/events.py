from src.models.questions_model import QuestionModel
from sqlalchemy import event
from sqlalchemy.orm.attributes import set_committed_value

def intercept_before_flush(session, flush_context, instances):
    print("this ran")
    for obj in session.new:
        if isinstance(obj, QuestionModel):
            if obj.questionKey is None:
                obj.questionKey = "set"

def intercept_after_flush(session, obj):
    if isinstance(obj, QuestionModel):
        print(obj)
        if obj.questionKey == "set":
            obj.set_questionKey()
            session.query(QuestionModel).filter_by(
                id = obj.id
            ).update(
                {
                    "questionKey": obj.questionKey
                }
            )
            set_committed_value(obj, "questionKey", obj.questionKey)
                


