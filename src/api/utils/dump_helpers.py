from src.database.utils.crud import(
   read_row_by_id,
   read_rows,
   create_rows,
   update_row_by_id,
   update_rows,
   delete_row_by_id,
   delete_rows
)

def get_one_row_by_id(session, model, id, dataConverter):
    """Return JSON representation of a row in a table
    first retreive mapped model from the db
    if the return size is 0, or more than 1, return no data with a fail
    if the return size is 1, continue
        using an implimentation of flask.json.JSONEncoder, process model into json
    Parameters
    ----------
    model
        sqlalchemy.ext.declarative.api.DeclativeMeta
        class that inherits the sqlalchemy.ext.declarative.Base, this is the class that is mapped to the data
    id
       int
       the primary key of the row selected
    Returns
    -------
    dict
       JSON serializable dict
    int
       HTTP status code of response
    """
    try:
        db_return = read_row_by_id(session, model, id).one()
        data, errors = dataConverter.dump(db_return)
        if bool(errors) == True:
            return {
                "error": {
                    "message": "An error has occured when producing the JSON",
                    "details": errors
                }
            }, 500
        return  data, 200
    except NoResultFound as e:
        return {"error": "no results found"}, 400
    except Exception as e:
        return {"error": repr(e)}, 500
def get_one_row_by_slug(session, model, slug, dataConverter):
    """Return JSON representation of a row in a table
    first retreive mapped model from the db
    if the return size is 0, or more than 1, return no data with a fail
    if the return size is 1, continue
        using an implimentation of flask.json.JSONEncoder, process model into json
    Parameters
    ----------
    model
        sqlalchemy.ext.declarative.api.DeclativeMeta
        class that inherits the sqlalchemy.ext.declarative.Base, this is the class that is mapped to the data
    slug
       str
       the slug of the row selected
    Returns
    -------
    dict
       JSON serializable dict
    int
       HTTP status code of response
    """
    try:
        db_return = read_rows(session, model,[{
            'slug':{
                'comparitor': '==',
                'data': slug
            }
        }]).one()
        dataConverter = dataConverter()
        data, errors = dataConverter.dump(db_return)
        if bool(errors) == True:
            return {
                "error": {
                    "message": "An error has occured when producing the JSON",
                    "details": errors
                }
            }, 500
        return  data, 200
    except NoResultFound as e:
        return {"error": "no results found"}, 400
    except Exception as e:
        return {"error": repr(e)}, 500

def get_all_rows(session, model, dataConverter, filters=None):
    """Return JSON representation of all rows in a table 
    first retreive all models from the db
    create an array to store jsonified version of each model
    for each model returned by the db
        using an implimentation of flask.json.JSONEnsrcr turn into json,
        add to the array
    return jsonified array with a success
    (if there are no models in the db it returns empty array with api_return:success)
    Parameters
    ----------
    model
        sqlalchemy.ext.declarative.api.DeclativeMeta
        class that inherits the sqlalchemy.ext.declarative.Base, this is the class that is mapped to the data
    Returns
    ------
    dict
        JSON serializable dict
    int
        HTTP status code of response
    """
    try:
        ##OPTOMIZATION REMARK##
        # good candidate for parrallel processing as IO bound
        db_return = read_rows(session, model, filters)
        return_obj = []
        dataConverter = dataConverter()
        #return_obj = dataConverter.dump(db_return)
        for row in db_return:
            data,errors = dataConverter.dump(row, many = False)
            if bool(errors) == True:
                return {
                    "error": {
                        "message": "An error has occured when producing the JSON",
                        "details": errors
                    }
                }, 500
            return_obj.append(
                data
            )
        return return_obj, 200
    except Exception as e:
        return {"error": repr(e)}, 500


def update_one_row_by_id(session, model, id, updates):
    try:
        update_row_by_id(session, model, id, updates)
    except ValueError as e:
        return {"error": repr(e)}, 400
    except NoResultFound as e:
        return {"error": repr(e)}, 400
    except Exception as e:
        return {"error": repr(e)}, 500
def update_one_row_by_slug(session, model, slug, updates):
    try:
        update_rows(session, model,updates,[{
            'slug': {
                'comparitor': '==',
                'data': slug
            }
        }])
    except ValueError as e:
        return {"error": repr(e)}, 400
    except NoResultFound as e:
        return {"error": repr(e)}, 400
    except Exception as e:
        return {"error": repr(e)}, 500

def update_selected_rows(session, model, updates, filters=None):
    try:
        update_rows(session, model, updates, filters)
    except Exception as e:
        return {"error": repr(e)}, 500


def create_one_row(session, model):
    try:
        create_row(session, model)
        return {}, 200
    except Exception as e:
        return {"error": repr(e)}, 500


def create_multiple_rows(session, *models):
    try:
        create_rows(session, *models)
        return {}, 200
    except Exception as e:
        return {"error": repr(e)}, 500


def delete_one_row_by_id(session, model, id):
    try:
        delete_row_by_id(session, model, id)
        return {}, 200
    except NoResultFound as e:
        return {"error": repr(e)}, 400
    except Exception as e:
        return {"error": repr(e)}, 500

def delete_one_row_by_slug(session, model, slug):
    try:
        delete_rows(session, model, [{
            'slug': {
                'comparitor': '==',
                'data': slug
            }
        }])
        return {}, 200
    except NoResultFound as e:
        return {"error": repr(e)}, 400
    except Exception as e:
        return {"error": repr(e)}, 500

def delete_selected_rows(session, model, filters=None):
    try:
        delete_rows(session, model, filters)
        return {}, 200
    except NoResultFound as e:
        return {"error": repr(e)}, 400
    except Exception as e:
        return {"error": repr(e)}, 500