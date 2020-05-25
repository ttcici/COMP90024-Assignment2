#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 23:37:32 2020

@author: ciciwang
"""


import json
import re


# /Users/ciciwang/Desktop/COMP90024_ASS2/analysis/aurin_data/data_used

"""
Load data and process data from AURIN
"""


satsf = json.load(open('/Users/ciciwang/Desktop/COMP90024_ASS2/analysis/aurin_data/data_used/satisfaction.json'))
pov = json.load(open('/Users/ciciwang/Desktop/COMP90024_ASS2/analysis/aurin_data/data_used/proverty.json'))

"""
grate satifaction:
satification score over 80 (100)
"""
satifaction_datasets = satsf['features']
life_grate_satisfaction = {}
population_sat_survey = {}
for ele in satifaction_datasets:
    satif_data = ele['properties']
    loc = satif_data["sa2_name16"]
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
    life_grate_satisfaction.update({ loc : grate_num })
    population_sat_survey.update({ loc : total_pop })
    
"""
proverty rate:
proportion of people with equivalised disposable household income 
after housing costs is below half median equivalised disposable household income 
after housing costs).
"""
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
    loc = pov_data["sa2_name16"]
    poverty_rate.update({ loc : pov_percent })
    houshold_income.update({ loc : inc_median})
    