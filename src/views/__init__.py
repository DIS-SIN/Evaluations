from flask import Flask


def register_views(app: Flask):
    from .survey_view import bp
    app.register_blueprint(bp)
    app.add_url_rule("/", endpoint="index")