from src.models.section_model import SectionModel
from src.models.sectionType_model import SectionTypeModel
from src.database import get_db
from marshmallow import Schema, post_load, validates_schema, ValidationError
from marshmallow.fields import Nested, Integer, String, Boolean

class SectionLoaderSchema(Schema):
    id = Integer()
    title = String()
    body = String()
    order = Integer()
    questions = Nested("QuestionLoaderSchema", many = True)
    subSections = Nested("self", many = True)
    type = String()

    @validates_schema
    def validates_schema(self, data):
        if data.get("id") is None:
            if data.get("type") is None:
                raise ValidationError("you must provide the type of the section",
                                      "type"
                                     )
    
    @post_load
    def load_section(self, data):
        session = get_db()
        if data.get("id") is not None:
            section = session.query(SectionModel).filter_by(
                id = data['id']
            ).one_or_none()
            if section is None:
                raise ValidationError(
                    f"The id {data[id]} for the section you have provided does not exist",
                    "id"
                )
        else:
            section = SectionModel()
        
        if data.get("title") is not None:
            section.title = data["title"]
        
        if data.get("body") is not None:
            section.body = data["body"]
        
        if data.get("type") is not None:
            sectionType = session.query(SectionTypeModel).filter_by(
                type = data["type"]
            ).one_or_none
            if sectionType is None:
                raise ValidationError(
                    "The type " + data["type"] +  "is not a valid section type" 
                )
            else:
                section.type = sectionType
        
        if data.get("questions") is not None:
            questions = [question['object'] for question in data['questions']]
            for question in section.questions and question.status == "active":
                if question not in questions:
                    question.status = "deactive"
            
            if data.get("subSections") is not None:
                subSections = [subSection["object"] for subSection in data['subSections']]
                for subSection in section.subSections:
                    if not subSection in subSections and subSection.status == "active":
                        subSection.status = "deactive"
                
                for subSection in data['subSections']:
                    if subSection['object'] not in section.subSections:
                        section.subSections.append(subSection['object'])
                    else:
                        subSection["object"].status = "active"
                    if subSection.get("order") is not None:
                            section.set_item_order(subSection["order"], subSection["object"])
            
            for question in data["questions"]:
                if question["object"] not in section.questions:
                    section.questions.append(question["object"])
                else:
                    question["object"].status = "active"
                if question.get("order") is not None:
                    section.set_item_order(question["order"], question["object"])
        elif data.get("subsections") is not None:
            subSections = [subSection["object"] for subSection in data['subSections']]
            for subSection in section.subSections:
                if not subSection in subSections and subSection.status == "active":
                    subSection.status = "deactive"
            
            for subSection in data['subSections']:
                if subSection['object'] not in section.subSections:
                    section.subSections.append(subSection['object'])
                else:
                    subSection["object"].status = "active"
                if subSection.get("order") is not None:
                        section.set_item_order(subSection["order"], subSection["object"])
        deserialized_return = {
            "object": section
        }
        if data.get("order") is not None:
            deserialized_return["order"] = data["order"]
        if section.type.type == "introduction":
            deserialized_return["introduction"] = True
        return deserialized_return

# TODO 
# check that the type of section in the subsections are not introduction or conclusion










            

