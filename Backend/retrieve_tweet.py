# Import the necessary methods from tweepy library
from tweepy import OAuthHandler
import config
import search_tweet_thread
import stream_tweet_thread

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

if __name__ == '__main__':
    stream_thread = stream_tweet_thread.get(auth)
    search_thread = search_tweet_thread.get(auth)

    stream_thread.start()
    search_thread.start()
