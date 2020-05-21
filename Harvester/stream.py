import json
import tweepy
import couchdb
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Open the geojson file of VIC Suburb/Locality Boundaries
# https://data.gov.au/dataset/ds-dga-af33dd8c-0534-4e18-9245-fc64440f742e/details
boundary = json.load(open('/Users/leo/Desktop/assignment2/vicgeo.json'))
 
# Create CouchDB dataset 
server = couchdb.Server("http://user:pass@172.26.130.158:5984")
#server = couchdb.Server("http://user:pass@localhost:5984")
#server.delete('temps')
if 'temps' in server:   
    db = server['temps']
else:
    db = server.create('temps') 

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
                                print(1)
                                for hashtag in tweetJson["extended_tweet"]["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["extended_tweet"]["full_text"], "hashtags": hashtags, "raw": tweetJson})
                            else:
                                print(2)
                                for hashtag in tweetJson["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["text"], "hashtags": hashtags, "raw": tweetJson})
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
                                print(3)
                                for hashtag in tweetJson["extended_tweet"]["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["extended_tweet"]["full_text"], "hashtags": hashtags, "raw": tweetJson})
                            else:
                                print(4)
                                for hashtag in tweetJson["entities"]["hashtags"]:
                                    hashtags.append(hashtag["text"])
                                db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["text"], "hashtags": hashtags, "raw": tweetJson})
                        # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                        except couchdb.http.ResourceConflict:
                            print("Duplicate tweets found and ignored.")
    
    def on_error(self, status_code):
        print(status_code)
                            
# Loop to save the tweets that meet the requirements in CouchDB , languages=["en"]
while True: 
    try:           
        myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
        myStream.filter(locations=[140.96190162,-39.19848673,150.03328204,-33.98079743], languages=["en"])
    except:
        continue