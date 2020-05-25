#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 15:02:44 2020

@author: ciciwang
"""

"""
city profile
"""
import json
import re
import couchdb






"""
Load bundaries info for suburb
"""
boundary = json.load(open('/Users/ciciwang/Desktop/COMP90024_ASS2/analysis/data_used/Melbourne.geojson'))
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
satsf = json.load(open('/Users/ciciwang/Desktop/COMP90024_ASS2/analysis/data_used/satisfaction.json'))
pov = json.load(open('/Users/ciciwang/Desktop/COMP90024_ASS2/analysis/data_used/proverty.json'))

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
Save data to CouchDB

"""

couch = couchdb.Server("http://user:pass@172.26.133.141:5984")
db_city = couch.create("city_profile")

# suburb.upper():  , doun
for suburb_name in sub_list:
    if suburb_name in coordinates:
        coordiantes =  coordinates[suburb_name] 
    else:
        coordiantes = "Undifined"
    if suburb_name in life_grate_satisfaction:
        satis = life_grate_satisfaction[suburb_name]
        pop =  population_sat_survey[suburb_name]
    else:
        satis = "Unknown"
        pop = "Unknown"
    if suburb_name in poverty_rate:
        pov_r = poverty_rate[suburb_name]
        med_i = houshold_income[suburb_name]
    else:
        pov_r = "Unknown"
        med_i = "Unknown"
    profile = {"boundaries": coordiantes,
                "num_grate_satisfcation" : satis,
                "population_survey" : pop,
                "poverty_rate" : pov_r,
                "houshold_median_income" : med_i}   
    #city_profile.update({ suburb_name.upper() : profile })
    
    db_city.save({ "_id" : suburb_name.upper(),
                  "profile": profile })
    
#print(list(city_profile.items())[0])
    
    
 
    













