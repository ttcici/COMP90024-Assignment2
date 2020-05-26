# This file includes the utilities can be used for back-end
# Team 16: COMP90024-Assignment2
# Team Members:
# Qingmeng Xu, 969413
# Tingqian Wang, 1043988
# Zhong Liao, 1056020
# Cheng Qian, 962539
# Zongcheng Du, 1096319

import couchdb
import config


# Connect to CouchDB
class ServerConnection:
    server = None

    def __init__(self):
        self.server = couchdb.Server(config.database_url)

    def get_db(self):
        return self.server


# View Result of database
class DatabaseConnection:
    database = None

    def __init__(self):
        self.database = couchdb.Server(config.database_url)

    def get_db(self, database_name):
        return self.database[database_name]

# Map Reduce
# class MapReduce:
#     def __init__(self):
#
#
#     def map(self):
#
#     def reduce(self):
