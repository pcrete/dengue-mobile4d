'''
Dengue Mobuile4D Missing Streets API

How to run

$ python3 index.py
'''
import json
import os
import urllib
import base64
import csv
import re
import pandas as pd

from flask import Flask, jsonify, request, abort
from flask import redirect, url_for, send_from_directory
from flask import render_template
from flask_cors import CORS, cross_origin
from flask_nav import Nav
from flask_nav.elements import *
from shapely.geometry import Polygon, Point, LineString, MultiLineString

from werkzeug.utils import secure_filename
from uuid import uuid4
from copy import deepcopy

from modules import gsvradar
from modules import missingboxradar

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
    
#import csv dengue-case
denguecase = pd.read_csv(os.path.join('static','dengue-cases','dengue-cases.csv'))
denguecase['addrcode'] = denguecase['addrcode'].astype(str)
    
#import Nakhon in subdistrict Shapefile
with open(
    os.path.join(
        'static',
        'dengue-cases',
        'Nakhon-subdistricts.geojson')
    ) as subdistrict_file:
    NakhonSubdistrict = json.load(subdistrict_file)

#import Nakhon in missing point shapefile
with open(
    os.path.join(
        'static',
        'missing-boxes',
        'Nakhon-Si-Thammarat-missing-boxes.geojson')
    ) as missingboxes_file:
    Nakhonmissingboxes = json.load(missingboxes_file)
    
    
'''
1. Request missing streets =========================================
'''

@app.route('/dengue/get/jobs/', methods=['POST'])
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
            print(json_respond)
            json_respond['data'] = target_streets
            return jsonify(json_respond)

    else:
        json_respond['status'] = 'error'
        json_respond['message'] = 'Request method != POST'
        print(json_respond)
        return jsonify(json_respond)

'''
2.1 Submit image urls to the server  =========================================
'''

@app.route('/dengue/send/urls/', methods=['POST'])
def get_image_urls():
    json_respond = {}
    if request.method == 'POST':
        data = request.json
        if data['geometry']['type'] != 'Point':
            json_respond['status'] = 'error'
            json_respond['message'] = 'Not a point geometry'
            print(json_respond)
            return jsonify(json_respond)

        lng, lat = data['geometry']['coordinates']

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

        if len(data['properties']['image_urls']) == 0:
            json_respond['status'] = 'error'
            json_respond['message'] = 'Empty image url'
            print(json_respond)
            return jsonify(json_respond)

        for ind, image_url in enumerate(data['properties']['image_urls']):
            try:
                resource = urllib.request.urlopen(image_url)
                destination = os.path.join(target, str(lat)+"_"+str(lng)+'_'+str(ind)+".jpg")
                output = open(destination,"wb")
                output.write(resource.read())
                output.close()
            except:
                json_respond['status'] = 'error'
                json_respond['message'] = 'Couldn\'t create upload directory: {}'.format(target)
                print(json_respond)
                return jsonify(json_respond)

        json_respond['status'] = 'success'
        json_respond['message'] = 'The images have been uploaded.'
        print(json_respond)
        return jsonify(json_respond)


'''
2.2 Submit base64 images to the server  =========================================
'''

@app.route('/dengue/send/base64/', methods=['POST'])
def get_encoded_images():
    json_respond = {}
    if request.method == 'POST':
        data = request.json
        if data['geometry']['type'] != 'Point':
            json_respond['status'] = 'error'
            json_respond['message'] = 'Not a point geometry'
            print(json_respond)
            return jsonify(json_respond)

        lng, lat = data['geometry']['coordinates']

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

        if len(data['properties']['base64_images']) == 0:
            json_respond['status'] = 'error'
            json_respond['message'] = 'Empty image url'
            print(json_respond)
            return jsonify(json_respond)

        for ind, base64_image in enumerate(data['properties']['base64_images']):
            try:

                destination = os.path.join(target, str(lat)+"_"+str(lng)+'_'+str(ind)+".jpg")
                with open(destination, 'wb') as fh:
                    fh.write(base64.b64decode(base64_image))

            except:
                json_respond['status'] = 'error'
                json_respond['message'] = 'Couldn\'t save image to directory: {}'.format(target)
                print(json_respond)
                return jsonify(json_respond)

        json_respond['status'] = 'success'
        json_respond['message'] = 'The images have been uploaded.'
        print(json_respond)
        return jsonify(json_respond)

'''
2.3 Submit photos to the server ======================================
'''

def allowed_file(filename):
      return '.' in filename and \
                   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/dengue/upload/images/', methods=['POST'])
def upload_file():
  json_respond = {}

  # check if it is POST method
  if request.method == 'POST':
      print()
      # check if the post request has the file part
      print(request.files)
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

      print(request.json)

      for upload in request.files.getlist("file"):
          filename = secure_filename(upload.filename.rsplit("/")[0])

          # if user does not select file, browser also
          # submit a empty part without filename
          if filename == '':
              json_respond['status'] = 'error'
              json_respond['message'] = 'No selected file'
              print(json_respond)
              return jsonify(json_respond)

          destination = os.path.join(target, filename)
          upload.save(destination)

          print("Accept incoming file:", filename)
          print("Save it to:", destination)

      # Success
      json_respond['status'] = 'success'
      json_respond['message'] = 'The images have been uploaded.'
      return jsonify(json_respond)

  else:
      json_respond['status'] = 'error'
      json_respond['message'] = 'Request method != POST'
      return jsonify(json_respond)

    

@app.route('/dengue/get/cases/', methods=['GET','POST'])
def dengue_cases():
    json_respond = {}
    
    data = request.json
    
    lng, lat = data['geometry']['coordinates']
    level = data['properties']['level']
    
    point = Point(lng,lat)
    TB_ID = 0
    AP_ID = 0
    totalPolygon = len(NakhonSubdistrict['features'])
    
    for i, feature in enumerate(NakhonSubdistrict['features']):
        poly = Polygon(NakhonSubdistrict['features'][i]['geometry']['coordinates'][0])
        if(poly.contains(point)):
            TB_ID = feature['properties']['TB_IDN']
            AP_ID = feature['properties']['AP_IDN']
            break
        elif i == totalPolygon - 1 :
            json_respond['status'] = 'error'
            json_respond['message'] = "The input point is invalid in the specific area"
            return jsonify(json_respond)
            break
    if level == 'subdistrict':
        subdist_count = denguecase.loc[denguecase['addrcode']== TB_ID]['cases'].sum()
        json_respond['status'] = 'success'
        json_respond['message'] = 'totalcases = '+str(subdist_count)
        json_respond['level'] = level
        return jsonify(json_respond)
    elif level == 'district':
        district_count = denguecase.loc[denguecase['addrcode'].str[:4]== AP_ID]['cases'].sum()
        json_respond['status'] = 'success'
        json_respond['message'] = 'totalcases = '+str(district_count)
        json_respond['level'] = level
        return jsonify(json_respond)
    
    
@app.route('/dengue/get/missing-boxes/', methods=['GET','POST'])
def dengue_get_missingboxes():
    json_respond = {}
    
    data = request.json
    
    lng, lat = data['geometry']['coordinates']
    
    target_streets = missingboxradar.by_radius(
    target_streets=deepcopy(Nakhonmissingboxes),
    lat=lat,
    lng=lng,
    radius=data['properties']['radius'],
    )
    
    if len(target_streets['features']) == 0:
        json_respond['status'] = 'error'
        json_respond['message'] = 'No missing-points found in the radius'
        return jsonify(json_respond)
    else:
        json_respond['status'] = 'success'
        json_respond['message'] = 'Missing-points found'
        print(json_respond)
        json_respond['data'] = target_streets
        return jsonify(json_respond)

'''
==================== Test API ===========================
'''
@app.route('/dengue/hello/')
@app.route('/dengue/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/dengue/foo/', methods=['GET','POST'])
def foo():
    data = request.json
    data['message'] = 'Hey'
    return json.dumps(data)

'''
=========================================================
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
