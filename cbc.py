import requests
import urllib.request
from textblob import TextBlob
import csv
import re
import json

cbc_stories = requests.get("https://www.cbc.ca/aggregate_api/v1/items?typeSet=cbc-ocelot&pageSize=28&page=1&lineupSlug=news-the-national&categorySlug=empty-category&source=Polopoly")
cbc_data1 = json.loads(cbc_stories.text)


def cbc_scrap():
    #Code to fetch the CTV Stories    
    with open("cbc_data.csv", 'w') as cbc_data:
        cbc_data.write("Title|Description|Polarity|Subjectivity\n")
        cbc_data.close()
    cbc_json = []

    for i in cbc_data1:
        description = i['description']
        title = i['title']
        x = TextBlob(description)
        p = "{0:.2f}".format(x.sentiment.polarity)
        s = "{0:.2f}".format(x.sentiment.subjectivity)
        # print(f"{description},{title},{p},{s}")
        with open("cbc_data.csv", 'a') as cbc_data:
            cbc_data.write(f"{description}|{title}|{p}|{s}\n")
        a = {
        't':title,
        'd':description,            
        'p':p,
        's':s
        }
        cbc_json.append(a)

    return cbc_json

