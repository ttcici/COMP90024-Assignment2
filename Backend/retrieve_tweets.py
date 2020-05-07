# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Enter Twitter API Keys
access_token = "1254430088793223168-EW9VjahphURxtfis4FHet6cqCeyMEB"
access_token_secret = "uCBT6FWhaTEPdMRweQRAEYHzBE7LVqfpUTtkoptRb3Vmi"
consumer_key = "be5MWgU3xxhxL3yXBW5P84vtL"
consumer_secret = "7KLLsiXLsR71arTnBwQNc14EDaE7UZrpsepINb4Q8UauLOjWb8"


# Create the class that will handle the tweet stream
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # Handle Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #TODO: tracklist is a list containing the words or hashtags you want to look for
    tracklist = None
    stream.filter(track=tracklist)
