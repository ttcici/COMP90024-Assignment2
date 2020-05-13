# This is the python program to run flask as the back-end. Default address: http://127.0.0.1:5000/
# Functionality: Get data from CouchDB as front-end requests, send the data back to front-end.
# Version: 1.0
# Last-update: 8/5/2020


from flask import Flask, jsonify
import requests
import utils
import config

app = Flask(__name__)


# Get doc from database by name
@app.route('/<string:name>', methods=['GET'])
def get_by_name(name):
    # r = requests.post("http://127.0.0.1:5555/", json.dumps({"1": "2"}))
    # return r.json()

    # for test:
    # cdb = [{1:2},{2:3}]
    cdb = utils.DatabaseConnection().get_db(name)
    response = {'name': name, 'data': []}

    for doc in cdb:
        response['data'].append(doc)
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=config.port)
