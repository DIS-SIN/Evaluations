from flask import Flask

def load_section_types(app: Flask):
    with app.app_context():
        from src.models.sectionType_model import SectionTypeModel
        from src.database import get_db
        
        session = get_db()

        greeting = SectionTypeModel(
            type = "greeting"
        )
        ending = SectionTypeModel(
            type = "ending"
        )
        group = SectionTypeModel(
            type = "group"
        )

        session.add(
            greeting
        )
        session.add(
            ending 
        )
        session.add(
            group
        )

        session.commit()
