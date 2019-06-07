
from flask import Flask, g
from sqlalchemy.orm.session import Session

def get_db() -> Session:
    from src.models.base_model import base
    if "scoped_session" not in g:
        g.scoped_session = base.session
    if "session" not in g:
        g.session = g.scoped_session()
    return g.session

def close_db(e):
    if "scoped_session" in g:
        scoped_session = g.pop('scoped_session')
        scoped_session.remove()
    if "session" in g:
        g.pop('session')

def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    from src.models import init_models
    from src.marshmallow import init_schemas
    init_models(app)
    init_schemas(app)

def init_db(app: Flask, mode: str):
    from src.models.base_model import base
    base.create_all()
    from .loaders.load_question_types import load_question_types
    from .loaders.load_section_types import load_section_types
    from .loaders.load_statuses import load_statuses
    from .loaders.load_departments import load_departments
    from .loaders.load_classification import load_classifications
    from .loaders.load_regions import load_regions
    load_question_types(app)
    load_statuses(app)
    load_departments(app)
    load_classifications(app)
    load_regions(app)
    load_section_types(app)
    

def delete_db():
    from src.models.base_model import base
    base.drop_all()

