from flask import Flask, jsonify
import base64
from flask import request as flask_request
import requests as py_request
import json

app = Flask(__name__)

request_URL = 'https://vision.googleapis.com/v1/images:annotate'

api_key = None
with open('API_KEY', "r") as key_file:
    api_key = key_file.read()

def imencode(image):
    return base64.b64encode(image.read())

def likelikessEnum(likeliness):
    if likeliness == 'VERY_UNLIKELY':
        return 1
    elif likeliness == 'UNLIKELY':
        return 2
    elif likeliness == 'POSSIBLE':
        return 3
    elif likeliness == 'LIKELY':
        return 4
    elif likeliness == 'VERY_LIKELY':
        return 5
    else:
        return 0

def weigh_expressions(expression_dict, i):
    joy = likelikessEnum(expression_dict['joyLikelihood'])
    sorrow = likelikessEnum(expression_dict['sorrowLikelihood'])
    anger = likelikessEnum(expression_dict['angerLikelihood'])
    surprise = likelikessEnum(expression_dict['surpriseLikelihood'])
    blurred = likelikessEnum(expression_dict['blurredLikelihood'])
    pan = expression_dict['panAngle']
    roll = expression_dict['rollAngle']
    tilt = expression_dict['tiltAngle']
    reason = ''
    expressions = True
    if blurred > 1:
        expressions = False
        reason += 'blurry'
    elif joy < 3:
        expressions = False
        reason += 'joyless'
    elif joy <= sorrow or joy <= anger or joy <= surprise:
        expressions = False
        reason += 'other_emotions'
    if reason != '':
        reason = 'face_' + str(i) + '_is_' + reason
    angles = True
    #expressions = 'joy=' + str(joy) + ' sorrow=' + str(sorrow) + ' anger=' + str(anger) + ' surprise=' + str(surprise) + ' blurred=' + str(blurred)
    #angles = 'deg_pan=' + str(pan) + ' deg_tilt=' + str(tilt) + ' roll=' + str(roll)
    return expressions, angles, reason

@app.route('/', methods=['POST', 'GET'])
def index():
    if flask_request.method == 'GET':
        return 'invalid'
    img = flask_request.files['image']
    encoded = imencode(img)
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
    req = py_request.post(url, data='', json=reqdata)
    if req.status_code == 200:
        data = req.json()
        faces = None
        try:
            faces = data['responses'][0]['faceAnnotations']
        except KeyError:
            pass
        if faces is None:
            return "faces=none"
        face_data = []
        reasons = ''
        i = 1
        for face in faces:
            exp, angle, reason = weigh_expressions(face, i)
            face_data.append(exp)
            face_data.append(angle)
            if reason != '':
                reasons += reason + ','
            i += 1
        if all(face_data):
            return 'faces=good'
        else:
            return 'faces=bad,' + reasons
    return(req.reason)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
