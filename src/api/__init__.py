from flask import Flask, Blueprint
from .utils.unicode_api import UnicodeApi
def register_routes(app: Flask):

    api_bp = Blueprint('api', __name__)
    api = UnicodeApi(api_bp, prefix= "/api", master_app= app)

    from .resources.survey_resource import SurveyResource
    from .resources.respondant_resource import RespondantResource
    api.add_resource(SurveyResource, '/surveys', '/surveys/<int:id>', '/surveys/slug/<string:slug>', endpoint = "surveys")
    api.add_resource(RespondantResource, '/respondants', '/respondants/<int:id>', '/respondants/slug/<string:slug>', endpoint = "respondants")
    app.register_blueprint(api_bp)
