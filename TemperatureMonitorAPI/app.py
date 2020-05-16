from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api

from api_resources.views import CreateNewClientWithJSONResource, CreateNewClientFormResource

# Create Flask API
app = Flask(__name__)
CORS(app)
api = Api(app, api_version='0.1')

"""
Add API resources to the GUIa
"""
# Add resources to the API
api.add_resource(CreateNewClientWithJSONResource, '/generate/file')
api.add_resource(CreateNewClientFormResource, '/generate/form')


@app.route('/')
def index():
    return """<head>
    <meta http-equiv="refresh" content="0; url=http://petstore.swagger.io/?url=http://localhost:5000/api/swagger.json" />
    </head>"""


if __name__ == '__main__':
    print('initiating Flask API...')
    app.run(debug=True, host='localhost', threaded=True)
