#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Team 16: COMP90024-Assignment2
# Team Members:
# Qingmeng Xu, 969413
# Tingqian Wang, 1043988
# Zhong Liao, 1056020
# Cheng Qian, 962539
# Zongcheng Du, 1096319

"""
Created on Sun May 24 21:41:09 2020

@author: ciciwang
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 01:20:56 2020

Initial Analysis on raw data 
detect the related words
label the sentiment

@author: ciciwang
"""

import time
import couchdb
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import re

"""
nltk function declaration
"""

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
lemmatizer = nltk.stem.WordNetLemmatizer()

#lemmatisation of the words from text
def lemmatisation(word):
    lemma = lemmatizer.lemmatize(word,'v')
    if lemma == word:
        lemma = lemmatizer.lemmatize(word,'n')
    return lemma

# applying lemmatisation to process text
def init_process(text) -> str:
    # lower cased
    text = text.lower()
    # tokenized
    words = tokenizer.tokenize(text)
    # check if word is alphabetic
    words = [w for w in words if w.isalpha()]
    # lemmatized 
    words = [lemmatisation(w) for w in words]

    init_processed_text = " ".join(words)
    return init_processed_text

# check whether the keyword in the text or not
def keyword_exist(processed_text, keyword_list) ->bool:
    for word in keyword_list:
        if word in processed_text:
            return True
    return False

#SentimentIntensityAnalyzer
def IdentifySentiment( sentence ): 
    sia = SentimentIntensityAnalyzer()
    ps = sia.polarity_scores( sentence )
    sentiment = max(ps, key = ps.get)
    return sentiment

def ScoringSentiment( sentence ): 
    si = SentimentIntensityAnalyzer()
    score = si.polarity_scores( sentence )
    return score


"""
Load related words list
"""

beers_wines_list = []
with open(
        "/home/ubuntu/analysis/beers.txt"
        , 'r', encoding="utf-8") as bw:
    bw_words = bw.readlines()
    for word in bw_words:
            word = lemmatisation(word)
            beers_wines_list.append(word.replace('\n',''))
        
sports_list = []
with open(
        "/home/ubuntu/analysis/sports.txt"
        , 'r', encoding="utf-8") as sp:
    sp_words = sp.readlines()
for word in sp_words:
    word = lemmatisation(word)
    sports_list.append(word.replace('\n',''))
        
coffee_list = []
with open(
        "/home/ubuntu/analysis/coffee.txt"
        , 'r', encoding="utf-8") as cf:
    cf_words = cf.readlines()
    for word in cf_words:
        word = lemmatisation(word)
        coffee_list.append(word.replace('\n',''))


"""
Load bundaries info for suburb
"""

boundary = json.load(open('/Users/ciciwang/Desktop/COMP90024_ASS2/analysis/Melbourne.geojson'))
sub_list=[ sub['properties']["sa2_name16"] for sub in boundary["features"] ]
coordinates={}
for sub in boundary["features"]:
    name = sub['properties']["sa2_name16"]
    bounda = sub["geometry"]["coordinates"]
    coordinates.update({ name : bounda })

"""
function defined to normalized a suburb name from a tweet data,
so as to match the suburb name in standard (boundary info) list,
and then to find the its coordianates from boundary data.
"""

def sub_name_normalized(tweet_suburb):
    for standard_sub in sub_list:
        if tweet_suburb.lower() == standard_sub.lower():
            return standard_sub
    for standard_sub in sub_list:
        if tweet_suburb.lower() in standard_sub.lower():
            return standard_sub
    for standard_sub in sub_list:
        if tweet_suburb.replace(" ", " - ").lower() == standard_sub.lower():
            return standard_sub
    for standard_sub in sub_list:
        if tweet_suburb.replace(" ", " - ").lower() in standard_sub.lower():
            return standard_sub
    for standard_sub in sub_list:
        if ('South' not in standard_sub
            ) and ('North' not in standard_sub
                   ) and ('West' not in standard_sub
                          ) and ('East' not in standard_sub):
            new = re.sub(r' South| North| West| East', '', tweet_suburb)
            if new.lower() == standard_sub.lower():
                return standard_sub
    for standard_sub in sub_list:
        if ('South' not in standard_sub
            ) and ('North' not in standard_sub
                   ) and ('West' not in standard_sub
                          ) and ('East' not in standard_sub):
            new = re.sub(r' South| North| West| East', '', tweet_suburb)
            if new.lower() in standard_sub.lower():
                return standard_sub
    return "Undifined"



"""
Load data and process data from AURIN

grate satisfaction:
satification score over 80 (100)

proverty rate:
proportion of people with equivalised disposable household income 
after housing costs is below half median equivalised disposable household income 
after housing costs).

"""
# data path
satsf = json.load(open('/Users/ciciwang/Desktop/COMP90024_ASS2/analysis/aurin_data/data_used/satisfaction.json'))
pov = json.load(open('/Users/ciciwang/Desktop/COMP90024_ASS2/analysis/aurin_data/data_used/proverty.json'))

# satisfaction
satisfaction_datasets = satsf['features']
life_grate_satisfaction = {}
population_sat_survey = {}
for ele in satisfaction_datasets:
    satif_data = ele['properties']
    if satif_data["_life_satisfaction_80_synth"] is None:
        satif_data["_life_satisfaction_80_synth"] = 0
    if satif_data["_life_satisfaction_90_synth"] is None:
        satif_data["_life_satisfaction_90_synth"] = 0
    if satif_data["_life_satisfaction_100_synth"] is None:
        satif_data["_life_satisfaction_100_synth"] = 0
    grate_num = satif_data["_life_satisfaction_80_synth"] + satif_data[
        "_life_satisfaction_90_synth"] + satif_data[
            "_life_satisfaction_100_synth"]
    total_pop = satif_data["total_pop_synth"]
    iloc = satif_data["sa2_name16"]
    loc = sub_name_normalized(iloc)
    life_grate_satisfaction.update({ loc : grate_num })
    population_sat_survey.update({ loc : total_pop })
    


proverty_datasets = pov['features']
poverty_rate = {}
houshold_income = {}
for elem in proverty_datasets:
    pov_data = elem["properties"]
    if pov_data["pov_rt_exc_hc_syn"] is None:
        pov_data["pov_rt_exc_hc_syn"] = 0
    if pov_data["inc_median_syn"] is None:
        pov_data["inc_median_syn"] = 0
    pov_percent = pov_data["pov_rt_exc_hc_syn"]
    inc_median = pov_data["inc_median_syn"]
    iloc = pov_data["sa2_name16"]
    loc = sub_name_normalized(iloc)
    poverty_rate.update({ loc : pov_percent })
    houshold_income.update({ loc : inc_median})

    


"""
Load data from CouchDB...
Create new database  
"""
id_list = []

while True:
    
    """
    Load data from CouchDB...
    Create new database or save updated data  
    """
    
    couch = couchdb.Server("http://user:pass@172.26.133.141:5984")
    db = couch['melb']
    #couch.delete('tweets_analyzed')
    if "tweets_analyzed" in couch:   
        db2 = couch["tweets_analyzed"]
    else:
        db2 = couch.create("tweets_analyzed")
        
    updated_tweets_list = []
    for doc_id in db:
        try:
            if doc_id not in id_list:
                #num_tweets += 1
                #print(num_tweets)
                tweet = db[doc_id]
                #tweets_id = doc_id
                suburb = tweet['suburb']
                text = tweet['text']
                id_list.append(doc_id)
                updated_tweets_list.append(
                    {'id':doc_id,
                    'suburb':suburb,
                    'text':text})
            else:
                continue
        except:
            break
        
        
    """
    word filter
    label sentiment
    update boundary
    label city life attributes of: life satisfaction and poverty rate
    """
    for tweets in updated_tweets_list:
        
        lemma_text = init_process(tweets['text'])
        if keyword_exist(lemma_text, beers_wines_list):
            tweets.update(
                {'bw_exist':1})
        else:
            tweets.update(
                {'bw_exist':0})
        if keyword_exist(lemma_text, sports_list):
            tweets.update(
                {'sp_exist':1})
        else:
            tweets.update(
                {'sp_exist':0})
        if keyword_exist(lemma_text, coffee_list):
            tweets.update(
                {'cf_exist':1})
        else:
            tweets.update(
                {'cf_exist':0})
            
        senti = IdentifySentiment(tweets['text'])
        scr = ScoringSentiment(tweets['text'])
        tweets.update({'sentiment': senti})
        tweets.update({'senti_score': scr})
        
        
        matched_suburb = sub_name_normalized(tweets['suburb'])
        
        # coordiantes
        if matched_suburb in coordinates:
            tweets.update({ 'bound' : coordinates[matched_suburb] })
        else:
            tweets.update({ 'bound': 'undifined'})
        
        #satisfaction
        if matched_suburb in life_grate_satisfaction:
            tweets.update({ 'num_grate_satis' : life_grate_satisfaction[matched_suburb]})
            tweets.update({ 'pop_survey' : population_sat_survey[matched_suburb] })
        else:
            tweets.update({ 'num_grate_satis' : 'Unkown' })
            tweets.update({ 'pop_survey' : 'Unkown' })
        
        #poverty
        if matched_suburb in poverty_rate:
            tweets.update({ 'poverty_rate' : poverty_rate[matched_suburb] })
            tweets.update({ 'houshold_income' : houshold_income[matched_suburb]})
        else:
            tweets.update({ 'poverty_rate' : 'Unkown' })
            tweets.update({ 'houshold_income' : 'Unkown'})
        
        
        try:
            db2.save({"_id": tweets['id'], 
                "suburb": tweets['suburb'], 
                "bw_exist": tweets['bw_exist'], 
                "sp_exist": tweets['sp_exist'], 
                "cf_exist": tweets['cf_exist'],
                "sentiment":tweets['sentiment'],
                "senti_score": tweets['senti_score'],
                "boundaries":tweets['bound'],
                "num_grate_satisfcation" : tweets['num_grate_satis'],
                "population_survey" : tweets['pop_survey'],
                "poverty_rate" : tweets['poverty_rate'],
                "houshold_median_income" : tweets['houshold_income']})
        except couchdb.http.ResourceConflict:
            print("Duplicate tweets found and ignored.")

    time.sleep(86400)

        




