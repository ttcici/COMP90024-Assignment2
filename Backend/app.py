# This is the python program to run flask as the back-end. Default address: http://127.0.0.1:8000/
# Functionality: Get data from CouchDB as front-end requests, send the data back to front-end.
# Version: 2.0
# Last-update: 22/5/2020
# Team 16: COMP90024-Assignment2
# Team Members:
# Qingmeng Xu, 969413
# Tingqian Wang, 1043988
# Zhong Liao, 1056020
# Cheng Qian, 962539
# Zongcheng Du, 1096319


from flask import Flask, jsonify
import utils
import config

app = Flask(__name__)


# Get doc from database by document name
@app.route('/database/<string:database_name>', methods=['GET'])
def get_by_name(database_name):
    cdb = utils.ServerConnection().get_db()[database_name]
    response = {'name': database_name, 'msg': None, 'data': []}

    for doc in cdb:
        response['data'].append(cdb[doc])

    response['msg'] = 'success'

    return jsonify(response)


# Get doc from database by predefined View
@app.route('/view/<string:database_name>/<string:view_id>/<string:view_name>/<int:group_level>', methods=['GET'])
def get_by_view(database_name, view_id, view_name, group_level):
    cdb = utils.DatabaseConnection().get_db(database_name)
    view_result = cdb.view(view_id + '/' + view_name, group_level=group_level).rows
    response = {'name': database_name, 'view': view_id + '/' + view_name, 'msg': None, 'data': []}

    for doc in view_result:
        response['data'].append(doc)

    response['msg'] = 'success'

    return jsonify(response)


# For connection test
@app.route('/', methods=['GET'])
def test():
    return {"res": "success"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.port)
