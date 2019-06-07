from flask import Flask

def load_question_types(app: Flask):
    with app.app_context():
        from src.models.questionTypes_model import QuestionTypeModel
        from src.database import get_db

        session = get_db()
        matrix = QuestionTypeModel(
            type = "matrix"
        )
        ranking = QuestionTypeModel(
            type = "ranking"
        )
        matrix_row = QuestionTypeModel(
            type = "matrix_row"
        )
        rank_row = QuestionTypeModel(
            type = "rank_row"
        )
        multiple_choice = QuestionTypeModel(
            type = "mcq"
        )
        dropdown = QuestionTypeModel(
            type = "dropdown"
        )
        radio = QuestionTypeModel(
            type = "radio"
        )
        text = QuestionTypeModel(
            type = "text"
        )
        session.add(
            matrix_row
        )
        session.add(
            rank_row
        )
        session.add(
            multiple_choice
        )
        session.add(
            dropdown
        )
        session.add(
            radio
        )
        session.add(
            text
        )
        session.commit()
        