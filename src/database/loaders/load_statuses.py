from flask import Flask

def load_statuses(app: Flask):
    with app.app_context():
        from src.database import get_db
        from src.models.status_model import StatusModel
        session = get_db()

        active = StatusModel(
            status="active",
            category="CONDUCTED_SURVEY"
        )
        closed = StatusModel(
            status="closed",
            category="CONDUCTED_SURVEY"
        )
        processing = StatusModel(
            status = "processing",
            category="CONDUCTED_SURVEY"
        )

        session.add(active)
        session.add(closed)
        session.add(processing)
        session.commit()

