import requests
import json

r = requests.post("http://127.0.0.1:5555/",json.dumps({"1":"2"}))
