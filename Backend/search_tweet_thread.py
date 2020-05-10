# Import the necessary methods from tweepy library
from tweepy import API
from threading import Thread


class get(Thread):
    def __init__(self, auth, query, couchdb, total_number):
        super().__init__()
        self.listener = StdOutListener()
        self.auth = auth
        self.api = API(auth_handler=self.auth, wait_on_rate_limit=true)
        self.total_number = total_number
        self.query = query
        self.couchdb = couchdb

    def run(self):
        count = 0
        while count < self.total_number:
            search_results = self.api.search(self.query, count=100)
            count += 100
            for tweet in search_results:
                # TODO: save tweet to CouchDB
                self.couchdb[''] = tweet
