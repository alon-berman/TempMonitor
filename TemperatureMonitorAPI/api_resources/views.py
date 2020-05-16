# import gevent  # can be used for production robustness

import multiprocessing

from flask import request
from flask_restful_swagger_2 import swagger, Resource

from api_resources.models import ErrorModel, ResponseModel
from ness_api.api_object import BusinessMonitor


class CreateNewClientWithJSONResource(Resource):
    """
    Specify GUI-related fields such as parameters, server requests etc.
    """

    @swagger.doc({
        'tags': ['create_new_client_with_json'],
        'description': 'Upload JSON file with client data.',
        'parameters': [
            {
                'name': 'client_data_json',
                'description': 'Upload client data',
                'in': 'query',
                'type': 'file',
                'required': True,
            }
        ],
        'responses': {
            '200': {
                'description': '',
                'schema': ResponseModel,
                'headers': {
                    'Location': {
                        'type': 'string',
                        'description': ''
                    }
                }
            }
        }
    })
    def post(self):
        """
        Use NessAPI to get a plugin by it's ID provided from the swagger GUI
        """
        # Validate request body with schema model
        try:
            monitor = multiprocessing.Process(target=BusinessMonitor, args=request.args['client_data_json'])
            monitor.start()
            return 'Upload Succeeded!', 200
        except Exception as e:
            return ErrorModel(**{'message': e.__str__()}), 400


class CreateNewClientFormResource(Resource):
    """
    Specify GUI-related fields such as parameters, server requests etc.
    """

    @swagger.doc({
        'tags': ['new_client_form'],
        'description': 'Set new monitor for client',
        'parameters': [
            {
                'name': 'business_name',
                'description': 'Enter Business Name',
                'in': 'query',
                'type': 'string',
                'required': True,
            },
            {
                'name': 'contact_name',
                'description': 'Enter Contact Name',
                'in': 'query',
                'type': 'string',
                'required': True,
            },
            {
                'name': 'contact_email',
                'description': 'Enter Contact Email',
                'in': 'query',
                'type': 'string',
                'required': False,
            },
            {
                'name': 'contact_phone',
                'description': 'Enter Contact Phone',
                'in': 'query',
                'type': 'string',
                'required': False,
            },
            {
                'name': 'cloud_server',
                'description': 'IOT Cloud Server Address',
                'in': 'query',
                'type': 'string',
                'required': False,
            },
            {
                'name': 'cloud_port',
                'description': 'IOT Cloud Server Port',
                'in': 'query',
                'type': 'string',
                'required': False,
            },
            {
                'name': 'app_id',
                'description': 'Application ID',
                'in': 'query',
                'type': 'string',
                'required': False,
            },
            {
                'name': 'access_key',
                'description': 'Application Access Key',
                'in': 'query',
                'type': 'string',
                'required': False,
            },
            {
                'name': 'minimum_temperature_thresh',
                'description': 'Fridge Temperature threshold',
                'in': 'query',
                'type': 'integer',
                'required': False,
            },
            {
                'name': 'maximum_temperature_thresh',
                'description': 'Fridge Temperature threshold.',
                'in': 'query',
                'type': 'integer',
                'required': False,
            },
            {
                'name': 'dev_id',
                'description': 'Device ID number',
                'in': 'query',
                'type': 'string',
                'required': False,
            },
            {
                'name': 'min_battery_volt_alert',
                'description': 'Minimum Battery Voltage Alert',
                'in': 'query',
                'type': 'integer',
                'required': False,
            },
            {
                'name': 'log_level',
                'description': 'Log Level',
                'in': 'query',
                'type': 'string',
                'required': False,
            },
            {
                'name': 'debug_mode',
                'description': 'Debug Mode - 0/1',
                'in': 'query',
                'type': 'integer',
                'required': False,
            },
            {
                'name': 'temp_stabilization_thresh',
                'description': 'Temperature Stabilization Thresh.',
                'in': 'query',
                'type': 'integer',
                'required': False,

            },
            {
                'name': 'time_between_alerts_sec',
                'description': 'Time between Alerts sec',
                'in': 'query',
                'type': 'integer',
                'required': False,
            }
        ],
        'responses': {
            '200': {
                'description': '',
                'schema': ResponseModel,
                'headers': {
                    'Location': {
                        'type': 'string',
                        'description': ''
                    }
                }
            }
        }
    })
    def get(self):
        """
        Use NessAPI to get a plugin by it's ID provided from the swagger GUI
        """
        # Validate request body with schema model
        try:
            monitor = BusinessMonitor(request.args)
            # monitor = multiprocessing.Process(target=BusinessMonitor, args=request.args)
            # monitor.start()
            return 'Succesfully created Monitor', 200
        except Exception as e:
            return ErrorModel(**{'message': e.__str__()}), 400
