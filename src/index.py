from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

@app.route('/foo', methods=['GET','POST'])
def foo():
    data = request.json
    data['respond'] = 'yes'
    return json.dumps(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)