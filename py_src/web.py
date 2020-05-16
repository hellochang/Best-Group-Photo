from flask import Flask
import base64
from flask import request

app = Flask(__name__)

def imencode(image):
    return base64.b64encode(image.read())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return 'invalid'
    else:
        return 'good'
