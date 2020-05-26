import json
import tweepy
import couchdb
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Open the geojson file of VIC Suburb/Locality Boundaries
# https://data.gov.au/dataset/ds-dga-af33dd8c-0534-4e18-9245-fc64440f742e/details
boundary = json.load(open('/home/ubuntu/leo/vicgeo.json'))
#boundary = json.load(open("/Users/leo/Desktop/assignment2/vicgeo.json"))
 
# Create CouchDB dataset 
server = couchdb.Server("http://user:pass@172.26.133.141:5984")
#server = couchdb.Server("http://user:pass@localhost:5984")
if 'melb' in server:   
    db = server['melb']
else:
    db = server.create('melb') 

# Authenticate to Twitter
auth = tweepy.OAuthHandler("ALNwJ7Unkb2WURTSDqA9o7Aan", "1vibUNGiegOhQa9WV1FzNGJdFFCyAclnOCna13sFGO9DMPhEWa")
auth.set_access_token("622442315-Mw1YibQ8XrkB0HvwNblH301Q5uSqV235yzR2P4An", "HNsNN5FYjjvWhK2VVVbnnKmttKePC0qp9JSbtgKYJxeGV")
api = tweepy.API(auth)
# Test authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

 
class MyStreamListener(tweepy.StreamListener):
    
    def on_data(self, data):
        print(1)
        result1 = False
        result2 = False
        result3 = False
        result4 = False
        tweetJson = json.loads(data)
        ID = str(tweetJson["id"])
        if tweetJson["place"]:
            if tweetJson["place"]["place_type"] == "neighborhood":
                place = tweetJson["place"]["name"]
                for suburb in boundary["features"]:
                    if suburb["properties"]["vic_loca_2"] == place.upper():
                        hashtags = []
                        # Save the tweet in CouchDB
                        try:
                            if "extended_tweet" in tweetJson:
                                for hashtag in tweetJson["extended_tweet"]["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["extended_tweet"]["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                print(ID)
                                result1 = True
                            else:
                                for hashtag in tweetJson["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["text"], "hashtags": hashtags, "raw": tweetJson})
                                print(ID)
                                result2 = True                        
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
                        # Save the tweet in CouchDB
                        try:
                            if "extended_tweet" in tweetJson:
                                for hashtag in tweetJson["extended_tweet"]["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["extended_tweet"]["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                result3 = True
                                print(ID)
                            else:
                                for hashtag in tweetJson["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["text"], "hashtags": hashtags, "raw": tweetJson})
                                result4 = True
                                print(ID)
                                # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                        except couchdb.http.ResourceConflict:
                            print("Duplicate tweets found and ignored.")
        maxid = str(int(ID) - 1)
        if result1 == True or result2 == True or result3 == True or result4 == True:
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
                        

    def on_error(self, status_code):
        print(status_code)
                            
# Loop to save the tweets that meet the requirements in CouchDB
while True: 
    try:           
        myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
        myStream.filter(locations=[140.96190162,-39.19848673,150.03328204,-33.98079743], languages=["en"])
                   
    except:
        continue