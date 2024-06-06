# -*- coding: utf-8 -*-
"""
Created on Thu May 23 22:02:16 2024

@author: Sven
"""



import requests
import json
import itertools
import csv


#######################################
#######################################
# SETTINGS


search_term = "game"

letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

alphanumberic = [chr(i) for i in range(ord('a'), ord('z') + 1)] + [str(i) for i in range(10)]
characters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
language = "en"
country = "us"

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,en-DE;q=0.6',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }

params = {
    'rpcids': 'teXCtc',
    'source-path': '/store/games',
    'f.sid': '6591558633047063482',
    'bl': 'boq_playuiserver_20240521.08_p0',
    'hl': language,
    'gl': country,
    'authuser': '0',
    'soc-app': '121',
    'soc-platform': '1',
    'soc-device': '1',
    '_reqid': '978784',
    'rt': 'c',
    }


#######################################
#######################################
# FUNCTIONS


def CombinationGenerator(characters, length):
    combinations = itertools.product(characters, repeat=length)
    combinations = [''.join(combination) for combination in combinations]
    
    return combinations


def CallGPSuggestAPI(search_term):
    data = 'f.req=%5B%5B%5B%22teXCtc%22%2C%22%5Bnull%2C%5B%5C%22' + search_term + '%5C%22%5D%2C%5B10%5D%2C%5B2%2C1%5D%2C4%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at=AHEfX0v2tcQRorogvL7a9C2LqJR3%3A1716493977115&'

    response = requests.post(
        'https://play.google.com/_/PlayStoreUi/data/batchexecute',
        params=params,
        headers=headers,
        data=data,
    )
    return response



#######################################
#######################################
# CALLS


combinations = CombinationGenerator(characters, 2)
print("len of char list: " + str(len(combinations)) + "")


result_list = []
counter = 0

for term in combinations:
    counter += 1
    print(str(counter) + "/" + str(len(combinations)))
    response = CallGPSuggestAPI(term)
    nested_keywords = json.loads(json.loads(response.text.splitlines()[3])[0][2])[0]
    for k in nested_keywords:
        result_list.append({
            "search_term" : term,
            "suggested_keyword" : k[0]})

print("Len result list")
print(len(result_list))

with open('result_list.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["search_term", "suggested_keyword"])
    writer.writeheader()
    writer.writerows(result_list)
