from flask import Flask, jsonify
import os 
from src.database import init_app, init_db, delete_db
from src.api import register_routes
from src.views import register_views
from flask_cors import CORS
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import warnings


def create_app(
    mode = "development",
    static_path = './static',
    templates_path = './templates',
    instance_path = "./instance"
    ) -> Flask:
    app = Flask(__name__)
    
    CORS(app)
    if os.path.isdir(instance_path):
        app.instance_path = os.path.abspath(instance_path)
    else:
        os.mkdir(instance_path)
        app.instance_path = os.path.abspath(instance_path)
    
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
        app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    else:
        # grab secret key from environment variable APP_SECRET_KEY   
        app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']
        # grab sqlalchemy database uri form the environment variable APP_SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['APP_SQLALCHEMY_DATABASE_URI']
        # grab the sentry url from the environment variable APP_SENTRY_URL
        # if the environment variable does not exist set sentry services to false
        sentry_url = os.environ.get("APP_SENTRY_URL")
        if sentry_url is None:
            app.config["SENTRY_SERVICES"] = False
            warnings.warn(
                "The environment variable APP_SENTRY_URL containing the url for the sentry client as described here "+
                "https://docs.sentry.io/platforms/python/flask/ was not provided as a result sentry services have been turned off"
            )
        else:
            app.config["SENTRY_SERVICES"] = True
            sentry_sdk.init(
                sentry_url,
                integrations = [FlaskIntegration()]
            )
            @app.route("/debug-sentry")
            def test_sentry():
                try:
                    something = 1/0
                except Exception as e:
                    sentry_sdk.capture_exception(e)
                    print(repr(e))
                return "Please look at your sentry client"
            
            print("Sentry is enabled to test your sentry configuration "+
                  "please access /debug-sentry you should see an error captured in sentry")



    # check if google api for natural language processing has been enabled by seeing if the environment varibale has been set
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
        app.config["NLP_SERVICES"] = False
        warnings.warn(
            "The google credentials were not set and as such NLP services have been turned off. Please set the path to the google credentials json "+
            "as decribed by the documentation https://cloud.google.com/natural-language/docs/reference/libraries#client-libraries-install-python"
        )
    else:
        app.config["NLP_SERVICES"] = True

        from google.cloud import language
        from google.cloud.language import enums
        from google.cloud.language import types
        
        @app.route("/debug-nlp")
        def test_nlp():
            try:
                client = language.LanguageServiceClient()
                text = u'The big brown fox went up the hill. He huffed and puffed and blew the houses down'
                document = types.Document(
                    content=text,
                    type=enums.Document.Type.PLAIN_TEXT
                )
                analysis = client.analyze_sentiment(document=document)
                sentences = []
                for sentence in analysis.sentences:
                    sentences.append(
                        {
                            "text": sentence.text.content,
                            "sentimentScore": sentence.sentiment.score,
                            "magnitudeScore": sentence.sentiment.magnitude
                        }
                    )
                return jsonify(
                    {
                        "language": analysis.language,
                        "sentimentScore": analysis.document_sentiment.score,
                        "magnitudeScore": analysis.document_sentiment.magnitude,
                        "sentences": sentences
                    }
                )
            except Exception as e:
                return "Execution failed with the following exception\n" + repr(e)


    app.config['JSON_AS_ASCII'] = False

    init_app(app)
    register_routes(app)
    register_views(app)

    @app.cli.command("init-db")
    def initialise_database():
        init_db(app, mode)
    @app.cli.command("delete-db")
    def wipe_database():
        delete_db()
    return app