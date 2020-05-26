import json
import couchdb
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Open the geojson file of VIC Suburb/Locality Boundaries
# https://data.gov.au/dataset/ds-dga-af33dd8c-0534-4e18-9245-fc64440f742e/details
boundary = json.load(open('/home/ubuntu/leo/vicgeo.json'))

# Create CouchDB dataset 
server = couchdb.Server("http://user:pass@172.26.133.141:5984")
#server = couchdb.Server("http://user:pass@localhost:5984")
#server.delete('temps')
if 'melb' in server:   
    db = server['melb']
else:
    db = server.create('melb') 
    
with open('/home/ubuntu/leo/twitter-melb.json', 'r', encoding = 'utf-8') as file:
    num = 0
    for line in file:
        num += 1
        print(num)
        line = line.replace('\n','').replace('\r','')
        try:
            if line[-1] == ',':
                tweetJson = json.loads(line[:-1])
                if tweetJson["doc"]["metadata"]["iso_language_code"] == "en":
                    ID = str(tweetJson["id"])
                    if tweetJson["doc"]["place"]:
                        if tweetJson["doc"]["place"]["place_type"] == "neighborhood":
                            place = tweetJson["doc"]["place"]["name"]
                            for suburb in boundary["features"]:
                                if suburb["properties"]["vic_loca_2"] == place.upper():
                                    hashtags = []
                                    # Save the tweet in CouchDB
                                    try:
                                        if "extended_tweet" in tweetJson["doc"]:
                                            for hashtag in tweetJson["doc"]["extended_tweet"]["entities"]["hashtags"]:
                                                hashtags.append(hashtag["text"])
                                            db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["doc"]["extended_tweet"]["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                        else:
                                            for hashtag in tweetJson["doc"]["entities"]["hashtags"]:
                                                hashtags.append(hashtag["text"])
                                            db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["doc"]["text"], "hashtags": hashtags, "raw": tweetJson})
                                    # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                    except couchdb.http.ResourceConflict:
                                        print("Duplicate tweets found and ignored.")
                    if tweetJson["doc"]["coordinates"]:
                        longitude = tweetJson["doc"]["coordinates"]["coordinates"][0]
                        latitude = tweetJson["doc"]["coordinates"]["coordinates"][1]
                        coordinate = Point(longitude, latitude)       
                        for suburb in boundary["features"]:
                            for multipolygon in suburb["geometry"]["coordinates"]:
                                if Polygon(multipolygon[0]).contains(coordinate):
                                    hashtags = []
                                    # Save the tweet in CouchDB
                                    try:
                                        if "extended_tweet" in tweetJson["doc"]:
                                            for hashtag in tweetJson["doc"]["extended_tweet"]["entities"]["hashtags"]:
                                                hashtags.append(hashtag["text"])
                                            db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["doc"]["extended_tweet"]["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                        else:
                                            for hashtag in tweetJson["doc"]["entities"]["hashtags"]:
                                                hashtags.append(hashtag["text"])
                                            db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["doc"]["text"], "hashtags": hashtags, "raw": tweetJson})
                                    # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                    except couchdb.http.ResourceConflict:
                                        print("Duplicate tweets found and ignored.")
            else:
                tweetJson = json.loads(line)
                if tweetJson["doc"]["metadata"]["iso_language_code"] == "en":
                    ID = str(tweetJson["id"])
                    if tweetJson["doc"]["place"]:
                        if tweetJson["doc"]["place"]["place_type"] == "neighborhood":
                            place = tweetJson["doc"]["place"]["name"]
                            for suburb in boundary["features"]:
                                if suburb["properties"]["vic_loca_2"] == place.upper():
                                    hashtags = []
                                    # Save the tweet in CouchDB
                                    try:
                                        if "extended_tweet" in tweetJson["doc"]:
                                            for hashtag in tweetJson["doc"]["extended_tweet"]["entities"]["hashtags"]:
                                                hashtags.append(hashtag["text"])
                                            db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["doc"]["extended_tweet"]["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                        else:
                                            for hashtag in tweetJson["doc"]["entities"]["hashtags"]:
                                                hashtags.append(hashtag["text"])
                                            db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["doc"]["text"], "hashtags": hashtags, "raw": tweetJson})
                                    # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                    except couchdb.http.ResourceConflict:
                                        print("Duplicate tweets found and ignored.")
                    if tweetJson["doc"]["coordinates"]:
                        longitude = tweetJson["doc"]["coordinates"]["coordinates"][0]
                        latitude = tweetJson["doc"]["coordinates"]["coordinates"][1]
                        coordinate = Point(longitude, latitude)       
                        for suburb in boundary["features"]:
                            for multipolygon in suburb["geometry"]["coordinates"]:
                                if Polygon(multipolygon[0]).contains(coordinate):
                                    hashtags = []
                                    # Save the tweet in CouchDB
                                    try:
                                        if "extended_tweet" in tweetJson["doc"]:
                                            for hashtag in tweetJson["doc"]["extended_tweet"]["entities"]["hashtags"]:
                                                hashtags.append(hashtag["text"])
                                            db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["doc"]["extended_tweet"]["full_text"], "hashtags": hashtags, "raw": tweetJson})
                                        else:
                                            for hashtag in tweetJson["doc"]["entities"]["hashtags"]:
                                                hashtags.append(hashtag["text"])
                                            db.save({"_id": ID, "suburb": suburb["properties"]["vic_loca_2"], "text": tweetJson["doc"]["text"], "hashtags": hashtags, "raw": tweetJson})
                                    # Check if the tweet already exists in the CouchDB to prevent duplicate storage
                                    except couchdb.http.ResourceConflict:
                                        print("Duplicate tweets found and ignored.")
        except Exception:
            continue