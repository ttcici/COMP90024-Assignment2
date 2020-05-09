# This is the python program to run flask as the back-end. Default address: http://127.0.0.1:5000/
# Functionality: Get data from CouchDB as front-end requests, send the data back to front-end.
# Version: 1.0
# Last-update: 8/5/2020

import json
from flask import Flask, request, jsonify
import requests
import couchdb

app = Flask(__name__)

# TODO: set CouchDB url
url = "172.26.0.0"

# Get doc from database by name
@app.route('/<string:name>', methods=['GET'])
def demo1(name):
    # r = requests.post("http://127.0.0.1:5555/", json.dumps({"1": "2"}))
    # return r.json()
    server = couchdb.Database(url)
    cdb = server['Databse name']
    doc = cdb[name]
    return jsonify(doc)

if __name__ == '__main__':
    app.run(port=8000)
