from marshmallow import Schema
from src.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from sentry_sdk import capture_message

def load_object(schema: Schema, json: dict):
    if json is None or bool(json) is False:
        return {
            "error": "must provide JSON for this request"
        }, 400
    result, errors = schema.load(json)
    if errors is not None and bool(errors) is True:
        return {
            "error":{
                "message": "The JSON schema you have sent is invalid",
                "details": errors
            }
        }, 400
    
    try:
        print(result)
        session = get_db()
        session.add(result)
        session.commit()
    except SQLAlchemyError as e:
        capture_message(e)
        return {
            "error": "An Internal Service Error has occured"
        }, 500
    
    return {},200



    

