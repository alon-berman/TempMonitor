from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def init():
    resp = request.data
    print(resp)
    return 'OK'


app.run(host='localhost', port=4005)