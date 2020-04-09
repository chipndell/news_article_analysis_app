import requests
# import pyodbc
import urllib.request
from textblob import TextBlob
from bs4 import BeautifulSoup as bs4
import csv
import re

# connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:socialfinal.database.windows.net,1433;Database=socialfinal;Uid=final;Pwd=admin1..;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

ctv_stories = requests.get("https://toronto.ctvnews.ca/more/local-news")
ctv_soup = bs4(ctv_stories.content, 'html.parser')


def ctv_scrap():
    # Code to fetch the CTV Stories    
    with open("ctv_data.csv", 'w') as ctv_data:
        ctv_data.write("Title|Description|Polarity|Subjectivity\n")
        ctv_data.close()

    # desc wrapping
    ctv_title = []
    ctv_titles = ctv_soup.find_all(class_="teaserTitle")  
    for x in ctv_titles:
        ctv_title.append(x.a.get_text())
        
    ctv_desc = []
    p_desc = []
    s_desc = []
    ctv_descs = ctv_soup.find_all('div',{"class":"lead-top teaserLead"})  
    for i in range(0,len(ctv_descs)):
        x = ctv_descs[i].find("p").get_text()
        y = re.split(r"\n",x)[1].strip()
        ctv_desc.append(y)
    #     print(ctv_desc.strip())
        ctv_desct = TextBlob(y)
        
        try:
            p = ctv_desct.sentiment.polarity
            p_desc.append(p)
        except:
            p = 0
            p_desc.append(p)
        try:
            s = ctv_desct.sentiment.subjectivity  
            s_desc.append(s)
        except:
            s = 0
            s_desc.append(s)
        
    m = zip(ctv_title,ctv_desc,p_desc,s_desc)   
    ctv_json = []
    for i in m:
        a = {
            't':i[0],
            'd':i[1],
            'p':i[2],
            's':i[3],
        }
        ctv_json.append(a)

    # title saving to csv
    # with open("ctv_data.csv", 'a') as ctv_data:
    #     for i in m:
    #         ctv_data.write(f"{i[0]}|{i[1]}|{i[2]}|{i[3]}\n")
    #         print(f":{i[0]}:{i[1]}:{i[2]}:{i[3]}:\n")
    #     ctv_data.close()


    return ctv_json


