# Import the necessary methods from tweepy library
from tweepy import OAuthHandler, StreamListener
from tweepy import Stream
from tweepy import API
import config
from threading import Thread


class get(Thread):
    def __init__(self, auth):
        super().__init__()
        self.listener = StdOutListener()
        self.auth = auth

    def run(self):
        stream = Stream(self.auth, self.listener)
        # TODO: tracklist is a list containing the words or hashtags you want to look for
        tracklist = None
        stream.filter(track=tracklist)


# Create the class that will handle the tweet stream
class StdOutListener(StreamListener):

    def on_data(self, data):
        # TODO: save data to CouchDB
        print(data)

    def on_error(self, status):
        print(status)
