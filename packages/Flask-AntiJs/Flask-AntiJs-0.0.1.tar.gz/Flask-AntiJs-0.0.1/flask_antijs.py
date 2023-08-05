import json

from flask import request
from werkzeug.exceptions import BadRequest


class AntiJs(object):

    def __init__(self, app=None, path_variables_only=False, ignore_payload=False, ignore_query_params=False):
        self.app = app
        if app is not None:
            self.init_app(app, path_variables_only, ignore_payload, ignore_query_params)

    def init_app(self, app, path_variables_only=False, ignore_payload=False, ignore_query_params=False):
        @app.before_request
        def check_for_undefined():
            if path_variables_only:  # Only check path variables
                for variable in request.view_args.values():
                    if variable == 'undefined':
                        raise BadRequest('\'undefined\' value found.')
            else:
                url = request.base_url if ignore_query_params else request.url
                if 'undefined' in url:  # Check entire url
                    raise BadRequest('\'undefined\' value found.')

                if not ignore_payload:
                    if request.is_json: # Check for json request
                        if 'undefined' in json.dumps(request.json):
                            raise BadRequest('\'undefined\' value found.')
                    else:
                        payload = request.form
                        for value in payload.values():
                            if value == 'undefined':
                                raise BadRequest('\'undefined\' value found.')