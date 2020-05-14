# This is the python program to run flask as the back-end. Default address: http://127.0.0.1:5000/
# Functionality: Get data from CouchDB as front-end requests, send the data back to front-end.
# Version: 1.0
# Last-update: 8/5/2020


from flask import Flask, jsonify
import utils
import config
import couchdb

app = Flask(__name__)


# Get doc from database by document name
@app.route('/<string:document_name>', methods=['GET'])
def get_by_name(document_name):
    # for test:
    # cdb = [{1:2},{2:3}]
    cdb = utils.DatabaseConnection().get_db(document_name)
    response = {'name': document_name, 'msg': None, 'data': []}

    for doc in cdb:
        response['data'].append(doc)
    response['msg'] = 'success'

    return jsonify(response)


if __name__ == '__main__':
    app.run(port=config.port)
