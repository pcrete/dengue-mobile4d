'''
Dengue Mobuile4D Missing Streets API

How to run

$ python3 index.py
'''
import json
import os

from flask import Flask, jsonify, request, abort
from flask import redirect, url_for, send_from_directory
from flask import render_template
from flask_cors import CORS, cross_origin
from flask_nav import Nav
from flask_nav.elements import *

from werkzeug.utils import secure_filename
from uuid import uuid4
from copy import deepcopy

from modules import gsvradar

'''
0. Initialization =================================================
'''

UPLOAD_FOLDER = os.path.join('static','uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# App configures
app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'A0Zr98j/3yX~XH~!DENGUE~!jmN]LWX/,?RT/MOBILE4D'

# import missing-streets file
with open(
	os.path.join(
		'static',
		'missing-streets',
		'Nakhon-Si-Thammarat-missing-streets.geojson')
	) as data_file:
	missing_streets = json.load(data_file)

'''
1. Request missing streets =========================================
'''

@app.route('/get/jobs/', methods=['POST'])
def get_jobs():
    json_respond = {}
    if request.method == 'POST':
        data = request.json
        if data['geometry']['type'] != 'Point':
            json_respond['status'] = 'error'
            json_respond['message'] = 'Not a point geometry'
            return jsonify(json_respond)

        lng, lat = data['geometry']['coordinates']

        target_streets = gsvradar.by_radius(
            target_streets=deepcopy(missing_streets),
            lat=lat,
            lng=lng,
            radius=data['properties']['radius'],
        )

        if len(target_streets['features']) == 0:
            json_respond['status'] = 'error'
            json_respond['message'] = 'No missing-streets found in the radius'
            return jsonify(json_respond)
        else:
            json_respond['status'] = 'success'
            json_respond['message'] = 'Missing-streets found'
            json_respond['data'] = target_streets
            return jsonify(json_respond)

    else:
        json_respond['status'] = 'error'
        json_respond['message'] = 'Request method != POST'
        return jsonify(json_respond)


'''
2. Submit photos to the server ======================================
'''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/images/', methods=['POST'])
def upload_file():
    json_respond = {}

    # check if it is POST method
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            json_respond['status'] = 'error'
            json_respond['message'] = 'No file part'
            print(json_respond)
            return jsonify(json_respond)

        print(request.files)

        # Create a unique "session ID" for this particular batch of uploads.
        upload_key = str(uuid4())
        target = os.path.join(app.config['UPLOAD_FOLDER'], upload_key)
        try:
            os.mkdir(target)
        except:
            json_respond['status'] = 'error'
            json_respond['message'] = 'Couldn\'t create upload directory: {}'.format(target)
            print(json_respond)
            return jsonify(json_respond)

        for upload in request.files.getlist("file"):
            filename = secure_filename(upload.filename.rsplit("/")[0])

            # if user does not select file, browser also
            # submit a empty part without filename
            if filename == '':
                json_respond['status'] = 'error'
                json_respond['message'] = 'No selected file'
                print(json_respond)
                return jsonify(json_respond)

            if upload and allowed_file(filename):

                destination = os.path.join(target, filename)
                upload.save(destination)

                print("Accept incoming file:", filename)
                print("Save it to:", destination)

            else:
                json_respond['status'] = 'error'
                json_respond['message'] = 'Not allowed file.'
                print(json_respond)
                return jsonify(json_respond)

        # Success
        json_respond['status'] = 'success'
        json_respond['message'] = 'The images have been uploaded.'
        return jsonify(json_respond)

    else:
        json_respond['status'] = 'error'
        json_respond['message'] = 'Request method != POST'
        return jsonify(json_respond)

'''
==================== Test API ===========================
'''
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/foo/', methods=['GET','POST'])
def foo():
    data = request.json
    print(data)
    return json.dumps(data)

'''
=========================================================
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
