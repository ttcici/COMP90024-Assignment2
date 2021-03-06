# Team 16: COMP90024-Assignment2
# Team Members:
# Qingmeng Xu, 969413
# Tingqian Wang, 1043988
# Zhong Liao, 1056020
# Cheng Qian, 962539
# Zongcheng Du, 1096319

import json
import tweepy
import couchdb
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import datetime
import time
import math

# Open the geojson file of VIC Suburb/Locality Boundaries
# https://data.gov.au/dataset/ds-dga-af33dd8c-0534-4e18-9245-fc64440f742e/details
boundary = json.load(open("/home/ubuntu/leo/vicgeo.json"))
 
# Create CouchDB dataset 
server = couchdb.Server("http://user:pass@172.26.133.141:5984")
#server = couchdb.Server("http://user:pass@localhost:5984")
#server.delete('tweets')
if "melb" in server:   
    db = server["melb"]
else:
    db = server.create("melb") 

keys = []
keys.append("HBA5V65VPUbOsxyDflGKYOs0S")
keys.append("be5MWgU3xxhxL3yXBW5P84vtL")
keys.append("rcFJ0DzhHSDvTfgHK49WMCc9S")
keys.append("L0BR4kmzsxaM7IdPUHdQ37Hns")
keys.append("jFgpCP4G99xyRMlB3mvSoNToB")
key = iter(keys)
secretkeys = []
secretkeys.append("3g7pu30kqviBOGrCGtRU0uQ7VmaUhoGVIpSbV2OMXe822aRXKQ")
secretkeys.append("7KLLsiXLsR71arTnBwQNc14EDaE7UZrpsepINb4Q8UauLOjWb8")
secretkeys.append("LZdhAUDVvnWcHHxUXTzYQF2f57KrNfmtEZHCmKzNZjxxsuG0Bp")
secretkeys.append("MsugIw8Ltx114Kkqgfm66RRpj7Z8KWqV1NR4Eq4xFFhkRGEJ67")
secretkeys.append("GGKrP8Xo8a4yLMwN5o94NvpyMFIQfDdDYxIGRHFo5pnmVRnthN")
secretkey = iter(secretkeys)
tokens = []
tokens.append("742178731351891969-Db6JwKM4oXaFn58HtsBCLTUfAwbNb5K")
tokens.append("1254430088793223168-2vNjv4WYXrfkvAnwxpmYvXDeJiL2SI")
tokens.append("1121779286069760000-UHzlxp96uTyQXjtHJFm5rLqzI0TRuH")
tokens.append("1118399076653944833-DUN8hDJDHqGka3lw6a29JNUi21qyaP")
tokens.append("987903261196734465-bm06Nhe1ryit2F3lJA3pS0tvdJQWZeX")
token = iter(tokens)
secrettokens = []
secrettokens.append("Qek3HT2AMT5h9WEzO8WxOBr7olJdypyzsIX75rYIBb4qc")
secrettokens.append("NjGEh6pK6oUru4WwndDzDdrIgms7zn5M8LY52Ryg1HQGK")
secrettokens.append("yHrsQCrFWzlHhSyoPetkRW0ACNu4mzpSq1YRPkdZzgaFL")
secrettokens.append("oXvl3HzDIvPJvLpr949pkD7nDxbxPsO9xoy1Lutl2P1Y7")
secrettokens.append("dwmaKwY2vTUmiayrRXN4o8kdeHxd4dFASEcMiQuG8ehzJ")
secrettoken = iter(secrettokens)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(next(key), next(secretkey))
auth.set_access_token(next(token), next(secrettoken))
api = tweepy.API(auth)
# Test authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    

#places = api.geo_search(query="Australia", granularity="country")
#place_id = places[0].id q="place:%s"%place_id, datetime.datetime.today().strftime("%Y-%m-%d")

maxID = None
num = 0
# Record the start time of each API
i = 0
start = [None]*len(keys)
start[i] = time.time()

# Loop to save the tweets that meet the requirements in CouchDB
while True: 
    try:
        if maxID == None:
            for tweet in tweepy.Cursor(api.search, geocode="-37.0201,144.9646,500km", until=datetime.datetime.today().strftime("%Y-%m-%d"), lang="en", tweet_mode="extended").items(500):
                result1 = False
                result2 = False
                num += 1
                print(num)
                tweetJson = tweet._json
                ID = str(tweet.id)
                if tweetJson["place"]:
                    if tweetJson["place"]["place_type"] == "neighborhood":
                        place = tweetJson["place"]["name"]
                        for suburb in boundary["features"]:
                            if suburb["properties"]["vic_loca_2"] == place.upper():
                                hashtags = []
                                for hashtag in tweetJson["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                # Save the tweet in CouchDB
                                try:
                                    db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                    result1 = True
                                # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                except couchdb.http.ResourceConflict:
                                    print("Duplicate tweets found and ignored.")
                if tweetJson["coordinates"]:
                    longitude = tweetJson["coordinates"]["coordinates"][0]
                    latitude = tweetJson["coordinates"]["coordinates"][1]
                    coordinate = Point(longitude, latitude)       
                    for suburb in boundary["features"]:
                        for multipolygon in suburb["geometry"]["coordinates"]:
                            if Polygon(multipolygon[0]).contains(coordinate):
                                hashtags = []
                                for hashtag in tweetJson["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                # Save the tweet in CouchDB
                                try:
                                    db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                    result2 = True
                                # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                except couchdb.http.ResourceConflict:
                                    print("Duplicate tweets found and ignored.")
                maxID = str(tweet.id - 1)
                maxid = maxID
                if result1 == True or result2 == True:
                    for tweet in tweepy.Cursor(api.user_timeline, user_id=tweetJson["user"]["id"], max_id=maxid, lang="en", tweet_mode="extended").items():
                        tweetJson = tweet._json
                        maxid = str(tweet.id)
                        if tweetJson["place"]:
                            if tweetJson["place"]["place_type"] == "neighborhood":
                                place = tweetJson["place"]["name"]
                                for suburb in boundary["features"]:
                                    if suburb["properties"]["vic_loca_2"] == place.upper():
                                        hashtags = []
                                        for hashtag in tweetJson["entities"]["hashtags"]:
                                            hashtags.append(hashtag["text"])
                                        # Save the tweet in CouchDB
                                        try:
                                            db.save({"_id": maxid, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                        # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                        except couchdb.http.ResourceConflict:
                                            print("Duplicate tweets found and ignored.")
                        if tweetJson["coordinates"]:
                            longitude = tweetJson["coordinates"]["coordinates"][0]
                            latitude = tweetJson["coordinates"]["coordinates"][1]
                            coordinate = Point(longitude, latitude)       
                            for suburb in boundary["features"]:
                                for multipolygon in suburb["geometry"]["coordinates"]:
                                    if Polygon(multipolygon[0]).contains(coordinate):
                                        hashtags = []
                                        for hashtag in tweetJson["entities"]["hashtags"]:
                                            hashtags.append(hashtag["text"])
                                        # Save the tweet in CouchDB
                                        try:
                                            db.save({"_id": maxid, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                        # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                        except couchdb.http.ResourceConflict:
                                            print("Duplicate tweets found and ignored.")
                        maxid = str(tweet.id - 1) 
        else:
            for tweet in tweepy.Cursor(api.search, geocode="-37.0201,144.9646,500km", until=datetime.datetime.today().strftime("%Y-%m-%d"), lang="en", max_id=maxID, tweet_mode="extended").items(500):
                result1 = False
                result2 = False
                num += 1
                print(num)
                tweetJson = tweet._json
                ID = str(tweet.id)
                if tweetJson["place"]:
                    if tweetJson["place"]["place_type"] == "neighborhood":
                        place = tweetJson["place"]["name"]
                        for suburb in boundary["features"]:
                            if suburb["properties"]["vic_loca_2"] == place.upper():
                                hashtags = []
                                for hashtag in tweetJson["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                # Save the tweet in CouchDB
                                try:
                                    db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                    result1 = True
                                # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                except couchdb.http.ResourceConflict:
                                    print("Duplicate tweets found and ignored.")
                if tweetJson["coordinates"]:
                    longitude = tweetJson["coordinates"]["coordinates"][0]
                    latitude = tweetJson["coordinates"]["coordinates"][1]
                    coordinate = Point(longitude, latitude)       
                    for suburb in boundary["features"]:
                        for multipolygon in suburb["geometry"]["coordinates"]:
                            if Polygon(multipolygon[0]).contains(coordinate):
                                hashtags = []
                                for hashtag in tweetJson["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                # Save the tweet in CouchDB
                                try:
                                    db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["full_text"],  "hashtags": hashtags, "raw": tweetJson})
                                    result2 = True
                                # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                except couchdb.http.ResourceConflict:
                                    print("Duplicate tweets found and ignored.")
                maxID = str(tweet.id - 1) 
                maxid = maxID
                if result1 == True or result2 == True:
                    for tweet in tweepy.Cursor(api.user_timeline, user_id=tweetJson["user"]["id"], max_id=maxid, lang="en", tweet_mode="extended").items():
                        tweetJson = tweet._json
                        maxid = str(tweet.id)
                        if tweetJson["place"]:
                            if tweetJson["place"]["place_type"] == "neighborhood":
                                place = tweetJson["place"]["name"]
                                for suburb in boundary["features"]:
                                    if suburb["properties"]["vic_loca_2"] == place.upper():
                                        hashtags = []
                                        for hashtag in tweetJson["entities"]["hashtags"]:
                                            hashtags.append(hashtag["text"])
                                        # Save the tweet in CouchDB
                                        try:
                                            db.save({"_id": maxid, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                        # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                        except couchdb.http.ResourceConflict:
                                            print("Duplicate tweets found and ignored.")
                        if tweetJson["coordinates"]:
                            longitude = tweetJson["coordinates"]["coordinates"][0]
                            latitude = tweetJson["coordinates"]["coordinates"][1]
                            coordinate = Point(longitude, latitude)       
                            for suburb in boundary["features"]:
                                for multipolygon in suburb["geometry"]["coordinates"]:
                                    if Polygon(multipolygon[0]).contains(coordinate):
                                        hashtags = []
                                        for hashtag in tweetJson["entities"]["hashtags"]:
                                            hashtags.append(hashtag["text"])
                                        # Save the tweet in CouchDB
                                        try:
                                            db.save({"_id": maxid, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                        # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                        except couchdb.http.ResourceConflict:
                                            print("Duplicate tweets found and ignored.")
                        maxid = str(tweet.id - 1) 
                
    # If rate limit is hit, switch to the next API
    except tweepy.error.TweepError as e:
			# Error Messages
            print(e)
            print("#" + str(i + 1) + " API hits rate limit (or other error), switching to next API.")
            # Switch to the next API
            if i == len(keys) - 1:
                key = iter(keys)
                secretkey = iter(secretkeys)
                token = iter(tokens)
                secrettoken = iter(secrettokens)
                i = 0
            else:
                i += 1 
            # Authenticate to Twitter
            auth = tweepy.OAuthHandler(next(key), next(secretkey))
            auth.set_access_token(next(token), next(secrettoken))
            api = tweepy.API(auth)
            # Test authentication 
            try:
                api.verify_credentials()
                print("Authentication OK")
            except:
                print("Error during authentication")

            if start[i] == None:
                start[i]  = time.time()
                print("Switched to #" + str(i + 1) + " API.")
                continue
            else:
                # Calculate the wait time on next API   
                wait = (15*60) - math.floor(time.time() - start[i]) 
                # Check if we need to wait
                if wait > 0:
                    time.sleep(wait)
                #Record the start time on next API
                start[i] = time.time()
                print("Switched to #" + str(i + 1) + " API.")
                continue
            
            

                    
