#! venv/bin python3
import os
from src import create_app

FLASK_ENV = os.environ.get('FLASK_ENV')

if FLASK_ENV is None or (FLASK_ENV != "production" and FLASK_ENV != "development"):
    mode = "production"
else:
    mode = FLASK_ENV


app = create_app( 
    mode,
    static_path= 'src/static',
    templates_path= 'src/templates'
)

if __name__ == "__main__":
    app.run('127.0.0.1', 5055)