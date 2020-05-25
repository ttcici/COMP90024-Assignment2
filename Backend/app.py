# This is the python program to run flask as the back-end. Default address: http://127.0.0.1:8000/
# Functionality: Get data from CouchDB as front-end requests, send the data back to front-end.
# Version: 2.0
# Last-update: 22/5/2020


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

# Get city profiles
@app.route('/geo', methods=['GET'])
def get_by_suburb():
    response = {"data": []}

    scdb = utils.DatabaseConnection().get_db('city_profile')
    cdb = utils.DatabaseConnection().get_db('analysis')
    bw_result = cdb.view('bw_view/bw_counts', group_level=1).rows
    cf_result = cdb.view('cf_view/cf_counts', group_level=1).rows
    sp_result = cdb.view('sp_view/sp_counts', group_level=1).rows

    tbw = 0
    tcf = 0
    tsp = 0

    i = 0
    for s in scdb:
        for bw in bw_result:
            if bw['key'] == s:
                tbw = bw['value']
                break
        for cf in cf_result:
            if cf['key'] == s:
                tcf = cf['value']
                break
        for sp in sp_result:
            if sp['key'] == s:
                tsp = sp['value']
                break

        geo = scdb[s]['profile']['boundaries']
        num_grate_satisfcation = scdb[s]['profile']['num_grate_satisfcation']
        population_survey = scdb[s]['profile']['population_survey']
        poverty_rate = scdb[s]['profile']['poverty_rate']
        houshold_median_income = scdb[s]['profile']['houshold_median_income']

        response['data'].append(
            {"type": "FeatureCollection", "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": geo},
                "properties": {
                    "suburb": "BRUNSWICK",
                    "bw_total": tbw,
                    "sp_total": tcf,
                    "cf_total": tsp,
                    "num_grate_satisfcation": num_grate_satisfcation,
                    "population_survey": population_survey,
                    "poverty_rate": poverty_rate,
                    "houshold_median_income": houshold_median_income}
            }]}
        )

        i += 1
        print(str(i)+' finished..')

    return jsonify(response)


# For connection test
@app.route('/', methods=['GET'])
def test():
    return {"res": "success"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.port)
