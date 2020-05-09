# Import the necessary methods from tweepy library
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import config
from threading import Thread


class get(Thread):
    def __init__(self,auth):
        super().__init__()
        self.listener = StdOutListener()
        self.auth = auth
        self.api = API(auth_handler=self.auth)

    def run(self):
        # TODO: save tweet to CouchDB
        search_result = self.api.search(tracklist)

