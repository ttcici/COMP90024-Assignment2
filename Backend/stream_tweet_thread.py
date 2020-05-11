# Import the necessary methods from tweepy library
from tweepy import StreamListener
from tweepy import Stream
from threading import Thread

count = 0


class get(Thread):

    def __init__(self, auth, query, couchdb, total_number):
        super().__init__()
        self.listener = StdOutListener(self.couchdb)
        self.auth = auth
        self.query = query
        self.couchdb = couchdb
        self.total_number = total_number

    def run(self):
        global count
        while count < self.total_number:
            stream = Stream(self.auth, self.listener)
            stream.filter(track=self.query)


# Create the class that will handle the tweet stream
class StdOutListener(StreamListener):
    def __init__(self, counchdb):
        super().__init__()
        self.couchdb = counchdb

    def on_data(self, data):
        # print(data)
        # Check duplicate
        if self.couchdb.get(data['id_str']) is None:
            # Save tweet to CouchDB
            global count
            count += 1
            self.couchdb[data['id_str']] = data

    def on_error(self, status):
        print(status)
