# This file includes the utilities can be used for back-end
# Version: 1.0
# Last-update: 9/5/2020

import couchdb
import config


# Connect to CouchDB
class DatabaseConnection:
    # TODO: set CouchDB url & database name
    server = None

    def __init__(self):
        self.server = couchdb.Database(config.database_url)

    def get_db(self, database_name):
        return self.server[database_name]

# Map Reduce
# class MapReduce:
#     def __init__(self):
#
#
#     def map(self):
#
#     def reduce(self):