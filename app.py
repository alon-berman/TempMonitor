from flask import Flask, request
from flask_restplus import Api, Resource, fields

import swagger.services.registration_service as registration_service
from BusinessMonitor.SeekNewClientLoop import MainLoop

flask_app = Flask(__name__)
app = Api(app=flask_app)

name_space = app.namespace('main', description='Main APIs')

model_business_details = app.model("business_details", {
    'business_name': fields.String(),
    'contact_name': fields.String(),
    'contact_email': fields.String(),
    'contact_phone': fields.String(),
})

model_device = app.model("devices", {
    'monitor_enabled': fields.Integer(),
    'device_id': fields.String(),
    'tag': fields.String(),
})

model_business = app.model('Init Model',
                           {
                               'business_details': fields.Nested(model_business_details),
                               'devices': fields.List(fields.Nested(model_device)),
                               'business_debug_mode': fields.Integer()
                           })


@name_space.route("/register")
class Register(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @app.expect(model_business)
    def post(self):
        data = request.json
        registration_service.register(data=data)


@name_space.route("/init-temp-monitor")
class InitTempMonitor(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    def post(self):
        MainLoop()

    def get(self):
        return {"status": "Successfully init flask server"}


flask_app.run(port=5000)
