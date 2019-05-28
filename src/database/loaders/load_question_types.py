from flask import Flask

def load_question_types(app: Flask):
    with app.app_context():
        from src.models.questionTypes_model import QuestionTypeModel
        from src.database import get_db

        session = get_db()
        matrix = QuestionTypeModel(
            type = "matrix"
        )
        multiple_choice = QuestionTypeModel(
            type = "mcq"
        )
        drop_down = QuestionTypeModel(
            type = "drop_down"
        )
        text = QuestionTypeModel(
            type = "text"
        )
        session.add(
            matrix
        )
        session.add(
            multiple_choice
        )
        session.add(
            drop_down
        )
        session.add(
            text
        )
        session.commit()
        