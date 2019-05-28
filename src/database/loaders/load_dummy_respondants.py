from flask import Flask

def load_dummy_respondants(app: Flask):
    with app.app_context():
        from src.database import get_db
        from src.models.departments_model import DepartmentModel
        from src.models.classification_model import ClassificationModel
        from src.models.regions_model import RegionModel
        from src.models.respondant_model import RespondantModel
        
        session = get_db()

        regions = session.query(RegionModel)
        departments = session.query(DepartmentModel)
        classifications = session.query(ClassificationModel)
        count_limit = 1000
        count = 0
        for region in regions:
            for department in departments:
                for classification in classifications:
                    respondant = RespondantModel(
                        session = session,
                        classification = classification,
                        department = department,
                        region = region
                    
                    )
                    session.add(respondant)
                    session.commit()
                    count += 1 
                    if count >= count_limit:
                        break



