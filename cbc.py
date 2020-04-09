import requests
# import pyodbc
import urllib.request
from textblob import TextBlob
import csv
import re
import json

# connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:socialfinal.database.windows.net,1433;Database=socialfinal;Uid=final;Pwd=admin1..;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
cbc_stories = requests.get("https://www.cbc.ca/aggregate_api/v1/items?typeSet=cbc-ocelot&pageSize=28&page=1&lineupSlug=news-the-national&categorySlug=empty-category&source=Polopoly")
cbc_data1 = json.loads(cbc_stories.text)


def cbc_scrap():
    #Code to fetch the CTV Stories    
    with open("cbc_data.csv", 'w') as cbc_data:
        cbc_data.write("Title|Description|Polarity|Subjectivity\n")
        cbc_data.close()
    cbc_json = []
    # with open("cbc_data.csv", 'a') as cbc_data:    
    #     for i in cbc_json:
    #         description = i['description']
    #         title = i['title']
    #         x = TextBlob(description)
    #         p = x.sentiment.polarity
    #         s = x.sentiment.subjectivity            
    #         # cbc_dataset.append(f"{description},{title},{p},{s}")
    #         cbc_data.write(f"{description}|{title}|{p}|{s}\n")
            
    #         a = {
    #         't':title,
    #         'd':description,            
    #         'p':p,
    #         's':s,
    #         }
    #         cbc_json.append(a)

    for i in cbc_data1:
        description = i['description']
        title = i['title']
        x = TextBlob(description)
        p = x.sentiment.polarity
        s = x.sentiment.subjectivity            
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

