from flask_restful_swagger_2 import Schema

"""
These classes define response and error models structure and types for the swagger UI.
"""


class ErrorModel(Schema):
    type = 'string'
    properties = {
        'message': {
            'type': 'string'
        }
    }


class ResponseModel(Schema):
    type = 'string'
    properties = {
        'message': {
            'type': 'string'
        }
    }
