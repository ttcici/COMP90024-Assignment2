import json
import tweepy
import couchdb
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import datetime
import time
import math

boundary = json.load(open("/Users/leo/Desktop/vicgeo.json"))
 
server = couchdb.Server("http://user:pass@localhost:5984")
#server.delete('temp')
if "tweet" in server:   
    db = server["tweet"]
else:
    db = server.create("tweet") 

keys = []
keys.append("HBA5V65VPUbOsxyDflGKYOs0S")
keys.append("be5MWgU3xxhxL3yXBW5P84vtL")
key = iter(keys)
secretkeys = []
secretkeys.append("3g7pu30kqviBOGrCGtRU0uQ7VmaUhoGVIpSbV2OMXe822aRXKQ")
secretkeys.append("7KLLsiXLsR71arTnBwQNc14EDaE7UZrpsepINb4Q8UauLOjWb8")
secretkey = iter(secretkeys)
tokens = []
tokens.append("742178731351891969-Db6JwKM4oXaFn58HtsBCLTUfAwbNb5K")
tokens.append("1254430088793223168-2vNjv4WYXrfkvAnwxpmYvXDeJiL2SI")
token = iter(tokens)
secrettokens = []
secrettokens.append("Qek3HT2AMT5h9WEzO8WxOBr7olJdypyzsIX75rYIBb4qc")
secrettokens.append("NjGEh6pK6oUru4WwndDzDdrIgms7zn5M8LY52Ryg1HQGK")
secrettoken = iter(secrettokens)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(next(key), next(secretkey))
auth.set_access_token(next(token), next(secrettoken))
api = tweepy.API(auth)
# test authentication , wait_on_rate_limit = True, wait_on_rate_limit_notify = True
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    

#places = api.geo_search(query="Australia", granularity="country")
#place_id = places[0].id

turn = 0
#maxID = "1260660092065558528"
maxID = None
start = [None]*len(keys)
i = 0
start[i] = time.time()

# https://data.gov.au/dataset/ds-dga-af33dd8c-0534-4e18-9245-fc64440f742e/details geocode="-37.0201,144.9646,500km",
#q="place:%s"%place_id,
while True:
    turn += 1
    print(turn)   
    try:
        if maxID == None:
            for tweet in tweepy.Cursor(api.search, geocode="-37.0201, 144.9646, 500km", until=datetime.datetime.today().strftime("%Y-%m-%d"), lang="en", tweet_mode="extended").items(500):
                tweetJson = tweet._json
                maxID = str(tweet.id)
                if tweetJson["place"]:
                    if tweetJson["place"]["place_type"] == "neighborhood":
                        place = tweetJson["place"]["name"]
                        for suburb in boundary["features"]:
                            if suburb['properties']["vic_loca_2"] == place.upper():
                                try:
                                    db.save({"_id": maxID, "suburb": suburb["properties"]["vic_loca_2"], "doc": tweetJson})
#                                    print(tweetJson["created_at"])
                                except couchdb.http.ResourceConflict:
                                    print("Duplicate tweets found and ignored.")
                elif tweetJson["coordinates"]:
                    longitude = tweetJson["coordinates"]["coordinates"][0]
                    latitude = tweetJson["coordinates"]["coordinates"][1]
                    coordinate = Point(longitude, latitude)       
                    for suburb in boundary["features"]:
                        for multipolygon in suburb["geometry"]["coordinates"]:
                            if Polygon(multipolygon[0]).contains(coordinate):
                                try:
                                    db.save({"_id": maxID, "suburb": suburb["properties"]["vic_loca_2"], "doc": tweetJson})
#                                    print(tweetJson["created_at"])
                                except couchdb.http.ResourceConflict:
                                    print("Duplicate tweets found and ignored.")
                maxID = str(tweet.id-1)
        else:
            for tweet in tweepy.Cursor(api.search, geocode="-37.0201, 144.9646, 500km", until=datetime.datetime.today().strftime("%Y-%m-%d"), lang="en", max_id=maxID, tweet_mode="extended").items(500):
                tweetJson = tweet._json
                maxID = str(tweet.id)
                if tweetJson["place"]:
                    if tweetJson["place"]["place_type"] == "neighborhood":
                        place = tweetJson["place"]["name"]
                        for suburb in boundary["features"]:
                            if suburb["properties"]["vic_loca_2"] == place.upper():
                                try:
                                    db.save({"_id": maxID, "suburb": suburb["properties"]["vic_loca_2"], "doc": tweetJson})
#                                    print(tweetJson["created_at"])
                                except couchdb.http.ResourceConflict:
                                    print("Duplicate tweets found and ignored.")
                elif tweetJson["coordinates"]:
                    longitude = tweetJson["coordinates"]["coordinates"][0]
                    latitude = tweetJson["coordinates"]["coordinates"][1]
                    coordinate = Point(longitude, latitude)       
                    for suburb in boundary["features"]:
                        for multipolygon in suburb["geometry"]["coordinates"]:
                            if Polygon(multipolygon[0]).contains(coordinate):
                                try:
                                    db.save({"_id": maxID, "suburb": suburb["properties"]["vic_loca_2"], "doc": tweetJson})
#                                    print(tweetJson["created_at"])
                                except couchdb.http.ResourceConflict:
                                    print("Duplicate tweets found and ignored.")
                maxID = str(tweet.id-1)
    except tweepy.error.TweepError as e:
			# Messages
            print(e)
            print("#", str(i+1), " API hits rate limit (or other error), switching to next API.")
            if i == len(keys) - 1:
                key = iter(keys)
                secretkey = iter(secretkeys)
                token = iter(tokens)
                secrettoken = iter(secrettokens)
                i = 0
            else:
                i += 1
            auth = tweepy.OAuthHandler(next(key), next(secretkey))
            auth.set_access_token(next(token), next(secrettoken))
            api = tweepy.API(auth)
            # test authentication 
            try:
                api.verify_credentials()
                print("Authentication OK")
            except:
                print("Error during authentication")

            if start[i] == None:
                start[i]  = time.time()
                continue
            else:                
                wait = (15*60) - math.floor(time.time() - start[i]) 
                if wait > 0:
                    time.sleep(wait)
                start[i] = time.time()
                print("Switched to #", str(i+1)," API.")
                server = couchdb.Server("http://user:pass@localhost:5984")
                db = server["tweet"]
                continue
            
            

                    