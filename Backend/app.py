from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return jsonify({
            "username": 'demo0'
        })

if __name__ == '__main__':
    app.run()
