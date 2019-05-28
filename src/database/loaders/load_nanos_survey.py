from flask import Flask

def load_nanos_survey(app: Flask):
    with app.app_context():
        from src.database import get_db
        from src.models.survey_model import SurveyModel
        from src.models.questions_model import QuestionModel
        from src.models.questionTypes_model import QuestionTypeModel
        
        session = get_db()
        
        mcq_question_type = session.query(QuestionTypeModel).filter_by(type="mcq").one()
        drop_down_question_type = session.query(QuestionTypeModel).filter_by(type="drop_down").one()
        text = session.query(QuestionTypeModel).filter_by(type="text").one()
        matrix = session.query(QuestionTypeModel).filter_by(type="matrix").one()


        survey = SurveyModel(
            title = "Learning Activity Evaluation Questionnaire",
            language = "en",
            description = """This questionnaire is designed to assess the quality of your learning experience with the Canada School of Public Service. Your responses will help us identify the factors that influence how you apply your learning back in the workplace. This way, learners, departments, and the School can work together to build a stronger government-wide learning culture.
            The information is being collected under the authority of paragraph 4(f) of the Canada School of Public Service Act and will be stored in the School’s evaluation system. Your personal information is protected under the Privacy Act. For more information, please refer to the School's Privacy Notice."""
        )

        session.add(survey)

        question_1 = QuestionModel(
            order = 1,
            question ='''Please rate your overall satisfaction or dissatisfaction with this learning activity on a scale of 1 to 10, 
            where 1 is "very dissatisfied" and 10 is "very satisfied".''',
            options = {
                "options": [
                    1,2,3,4,5,6,7,8,9,10
                ]
            },
            questionType = mcq_question_type

        )
        session.add(question_1)

        survey.questions.append(question_1)

        session.commit()