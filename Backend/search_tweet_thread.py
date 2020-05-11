# Import the necessary methods from tweepy library
from tweepy import API
from threading import Thread

class Get(Thread):
    def __init__(self, auth, query, couchdb, total_number):
        super().__init__()
        self.auth = auth
        self.api = API(auth_handler=self.auth, wait_on_rate_limit=True)
        self.total_number = total_number
        self.query = query
        self.couchdb = couchdb

    def run(self):
        count = 0
        while count < self.total_number:
            search_results = self.api.search(self.query, count=100)
            count += 100
            for tweet in search_results:
                json_data = tweet._json
                print('From Search')
                print(json_data)
                # Check duplicate
                if self.couchdb.get(json_data['id_str']) is None:
                    # Save tweet to CouchDB
                    self.couchdb[json_data['id_str']] = json_data
