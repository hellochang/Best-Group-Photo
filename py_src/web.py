from flask import Flask, jsonify
import base64
from flask import request as flask_request
import requests as py_request
import json

app = Flask(__name__)

img = open("20180322_150321_HDR.jpg", "rb") #test

#print(type(img))
#print(len(img))

request_URL = 'https://vision.googleapis.com/v1/images:annotate'

api_key = None
with open('API_KEY', "r") as key_file:
    api_key = key_file.read()

def imencode(image):
    return base64.b64encode(image.read())

imgdata = imencode(img)

@app.route('/', methods=['GET', 'POST'])
def index():
    encoded = imgdata
    reqdata={
    "requests":[
        {
            "image":{
                "content":encoded.decode("utf-8")
                },
                "features":[
                    {
                        "type":"FACE_DETECTION",
                        "maxResults":20
                    }
                ]
            }
        ]
    }
    url = request_URL + '?key=' + api_key
    #print(jsonify(reqdata))
    req = py_request.post(url, data='', json=reqdata)
    with open('out.txt', "w") as debug_file:
        debug_file.write(json.dumps(req.json()))
    if req.status_code == 200:
        return json.dumps(req.json())
    return(req.reason)
