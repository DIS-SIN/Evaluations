from marshmallow import Schema, post_load, ValidationError, validates, validates_schema
from marshmallow.fields import Nested, String, Integer, Nested
from src.database import get_db
from src.models.survey_model import SurveyModel

class SurveyLoaderSchema(Schema):
    id = Integer()
    title = String()
    description = String()
    language = String()
    questions = Nested("QuestionLoaderSchema", many=True)

    @validates("language")
    def validate_language_options(self, value):
        if value != "en" and value != "fr":
            raise ValidationError(
                f"language must be either en or fr: {value} is not supported"
            )
    
    @validates_schema
    def validate_schema(self, data):
        if data.get("id") is None and data.get("slug") is None:
            if data.get("title") is None or data.get("title") == "":
                raise ValidationError(
                    "title field must not be none or empty"
                )
            if data.get("description") is None or data.get("description") == "":
                raise ValidationError(
                    "description field must not be none or empty"
                )
            questions =  data.get("questions")
            sections = data.get("sections")

            if (questions is None or questions == []) and (sections is None or sections == []):
                raise ValidationError(
                    "at least one question or section is needed to create a survey",
                    "questions",
                    "sections"
            )
        if data.get("id") is not None and data.get("slug") is not None:
            raise ValidationError(
                "id and slug field must not be empty "
            )

    @post_load
    def make_survey(self, data):
        session = get_db()
        if data.get("id") is not None:
            survey = session.query(SurveyModel).filter_by(id = data["id"]).one_or_none()
            if survey is None:
                raise ValidationError(
                    f"Could not find survey with the following id: " + str(data["id"])
                )
        elif data.get("slug") is not None:
            survey = session.query(SurveyModel).filter_by(slug = data["slug"]).one_or_none()
            if survey is None:
                raise ValidationError(
                    f"Could not find survey with the following slug: " + str(data["slug"])
                )
        else:
            survey = SurveyModel(session = session)
        
        if data.get("title") is not None:
            survey.title = data['title']
        
        if data.get("description") is not None:
            survey.description = data['description']
        
        if data.get("language") is not None:
            survey.language = data['language']
        
        if data.get("questions") is not None:
            questions = [question["object"] for question in data["questions"]]
            for question in questions:
                if question not in survey.questions:
                    survey.questions.append(question)
            
            for survey_question in survey.questions:
                if survey_question not in questions:
                    survey.questions.remove(survey_question)

            if data.get("sections") is not None:
                sections = [section["object"] for section in data["sections"]]
                for section in sections:
                    if section not in survey.sections:
                        survey.sections.append(section)

                for survey_section in survey.sections:
                    if survey_section not in sections:
                        survey.sections.remove(survey_section)
                    
                for section in data["sections"]:
                    if section.get("order") is not None:
                        survey.set_item_order(section["order"], section["object"])
                
            for question in data["questions"]:
                if question.get("order") is not None:
                    survey.set_item_order(question["order"], question["object"])

        elif data.get("sections") is not None:
            sections = [section["object"] for section in data["sections"]]
            for section in sections:
                if section not in survey.sections:
                    survey.sections.append(section)

            for survey_section in survey.sections:
                if survey_section not in sections:
                    survey.sections.remove(survey_section)
            
            for section in data["sections"]:
                if section.get("order") is not None:
                    survey.set_item_order(section["order"], section["object"])
             
        return survey





