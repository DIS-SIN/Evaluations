from flask_restful import Api

class UnicodeApi(Api):
    def __init__(self, *args, master_app, **kwargs):
        super(UnicodeApi, self).__init__(*args, **kwargs)
        master_app.config['RESTFUL_JSON'] = {
            'ensure_ascii': False
        }
        