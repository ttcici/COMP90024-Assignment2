from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def demo():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return jsonify({
            "username": 'demo0'
        })

@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        r = request.post

if __name__ == '__main__':
    app.run()
