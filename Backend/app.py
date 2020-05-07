import json
from flask import Flask, request, jsonify
import requests
import couchdb

app = Flask(__name__)


@app.route('/', methods=['POST'])
def demo():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return jsonify({
            "username": 'demo0'
        })


@app.route('/', methods=['GET'])
def demo1():
    r = requests.post("http://127.0.0.1:5555/", json.dumps({"1": "2"}))
    print(r.json())

if __name__ == '__main__':
    app.run()
