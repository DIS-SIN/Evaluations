from flask import Flask
import os 
from src.database import init_app, init_db, delete_db
def create_app(
    mode = "development",
    static_path = './static',
    templates_path = './templates'
    ) -> Flask:
    app = Flask(__name__)
    if os.path.isdir(static_path):
        app.static_folder = os.path.abspath(static_path)
    else:
        raise ValueError(f'static_path {static_path} is not a valid path')
    
    if os.path.isdir(templates_path):
        app.template_folder = os.path.abspath(templates_path)
    else:
        raise ValueError(f"templates_path {templates_path} is not a valid path")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if mode == "development":
        app.config['SECRET_KEY'] = "so secret"
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:password@localhost:5432/evaluations"
    else:
        app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['APP_SQLALCHEMY_DATABASE_URI']
    init_app(app)

    @app.cli.command("init-db")
    def initialise_database():
        init_db(app)
    @app.cli.command("delete-db")
    def wipe_database():
        delete_db()
    return app