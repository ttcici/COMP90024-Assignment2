# This is the python program to run flask as the back-end. Default address: http://127.0.0.1:8000/
# Functionality: Get data from CouchDB as front-end requests, send the data back to front-end.
# Version: 2.0
# Last-update: 22/5/2020


from flask import Flask, jsonify
import utils
import config

app = Flask(__name__)

# Get doc from database by document name
@app.route('/<string:database_name>', methods=['GET'])
def get_by_name(database_name):
    cdb = utils.DatabaseConnection().get_db()[database_name]
    response = {'name': database_name, 'msg': None, 'data': []}

    for doc in cdb:
        response['data'].append(cdb[doc])

    response['msg'] = 'success'

    return jsonify(response)

# For connection test
@app.route('/', methods=['GET'])
def test():
    return {"res": "success"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.port)
