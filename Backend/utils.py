# This file includes the utilities can be used for back-end
# Version: 1.0
# Last-update: 9/5/2020

import couchdb
from tweepy import StreamListener


# Connect CouchDB
class DatabaseConnection:
    # TODO: set CouchDB url & database name
    url = "172.26.0.0"
    db_name = 'Databse name'
    server = None

    def __init__(self):
        self.server = couchdb.Database(self.url)

    def get_db(self):
        return self.server[self.db_name]


# Create the class that will handle the tweet stream
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)
