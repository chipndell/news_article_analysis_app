import requests
import urllib.request
from textblob import TextBlob
from bs4 import BeautifulSoup as bs4
import csv

ctv_stories = requests.get("https://toronto.ctvnews.ca/more/local-news")
ctv_soup = bs4(ctv_stories.content, 'html.parser')


def ctv_scrap():   
    article = ctv_soup.find_all(class_="dc")    
    ctv_json = []
    # print(ctv_titles)
    for x in range(0,len(article)):        
        title = article[x].find('h2', class_="teaserTitle").find('a').get_text()
        for y in range(0,len(article)):
            desc = ctv_soup.find('div',class_="lead-top teaserLead").find('p').get_text().strip().split('\n')[0]
            t_blob = TextBlob(desc)
            try:
                p = t_blob.sentiment.polarity        
            except:
                p = 0        
            try:
                s = t_blob.sentiment.subjectivity       
            except:
                s = 0.5
        data = {"t":title,"d":desc,"p":p,"s":s}
        ctv_json.append(data)
    # Code to write the CTV Stories to csv
    # with open("ctv_data.csv", 'w') as ctv_data:
    #     ctv_data.write("Title|Description|Polarity|Subjectivity\n")
    #     ctv_data.close() 
    # with open("ctv_data.csv", 'a') as ctv_data:
    #     for i in m:
    #         ctv_data.write(f"{i[0]}|{i[1]}|{i[2]}|{i[3]}\n")
    #     ctv_data.close()
    
    return ctv_json
