# Import the necessary methods from tweepy library
from tweepy import OAuthHandler
import config
import search_tweet_thread
import stream_tweet_thread
import utils

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

if __name__ == '__main__':
    cdb = utils.DatabaseConnection().get_db()
    # for test:
    # cdb = None
    stream_thread = stream_tweet_thread.Get(auth, config.query, cdb, config.stream_number)
    search_thread = search_tweet_thread.Get(auth, config.query, cdb, config.search_number)

    stream_thread.start()
    search_thread.start()
