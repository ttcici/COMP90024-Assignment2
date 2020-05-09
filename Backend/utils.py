# This file includes the utilities can be used for back-end
# Version: 1.0
# Last-update: 9/5/2020

import couchdb


class DatabaseConnection:
    # TODO: set CouchDB url & database name
    url = "172.26.0.0"
    db_name = 'Databse name'
    server = None

    def __init__(self):
        self.server = couchdb.Database(self.url)

    def get_db(self):
        return self.server[self.db_name]
