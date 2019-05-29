from flask_restful import Resource
from src.models.surveySchemaless_model import SurveySchemalessModel
from src.marshmallow.surveySchemaless_schema import SurveySchemalessSchema
from src.database import get_db
from flask import request
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

class SurveySchemalessResource(Resource):

    def get(self):
        session = get_db()
        surveys = session.query(
            SurveySchemalessModel
        ).all()
        survey_dump = []
        for survey in surveys:
            survey_dump.append(
                SurveySchemalessSchema(only = ('survey',)).dump(
                    survey
                ).data['survey']
            )
        return survey_dump, 200
    def post(self):
        session = get_db()
        client = language.LanguageServiceClient()
        json = request.get_json()
        if json is None:
            return {
                "error": "No JSON posted"
            }, 400
        keys = list(json.keys())
        for key in keys:
            if "textarea" in key:
                text = u''+json.get(key)
                document = types.Document(
                    content=text,
                    type=enums.Document.Type.PLAIN_TEXT
                )
                sentiment = client.analyze_sentiment(document=document)
                json[key + "_sentimentScore"] = sentiment.document_sentiment.score
                json[key + "_magnitudeScore"] = sentiment.document_sentiment.magnitude
                json[key + "_language"] = sentiment.language
                sentences = []
                for sentence in sentiment.sentences:
                    sentence_dict = {
                        'text': sentence.text.content,
                        'sentimentScore': sentence.sentiment.score,
                        'magnitudeScore': sentence.sentiment.magnitude
                    }
                    sentences.append(sentence_dict)
                json[key + "_sentences"] = sentences


        survey = SurveySchemalessModel(
            survey = json
        )
        session.add(survey)
        session.commit()
        return SurveySchemalessSchema(only = ("survey", )).dump(
            survey
        ).data['survey'], 200

    def delete(self):
        session = get_db()
        session.query(SurveySchemalessModel).delete()
        session.commit()
        return {}, 201
        


