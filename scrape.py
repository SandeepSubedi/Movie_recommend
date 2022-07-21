from multiprocessing import get_all_start_methods
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import os

os.system('clear')

def get_all_titles(soup):
    result_topics=[]
    all_topics=soup.find_all('h3',{"class":"lister-item-header"})
    #print(all_topics)
    for topic in all_topics:
        topic=str(topic.find('a'))
        topic=topic.replace("<","=")
        topic=topic.replace(">","=")
        topic=topic.split('=')
        topic=topic[int(len(topic)/2)] 
        result_topics.append(topic)
    return result_topics

def get_all_genres(soup):
    result_genres=[]
    all_genres=soup.find_all("p",{"class":'text-muted'})
    #print(all_genres)
    for genre in all_genres:
        genre=str(genre.find_all("span",{"class":"genre"}))
        #print(genre)
        if genre=='[]':
            pass
        else:
            genre=genre.replace("<","=")
            genre=genre.replace(" ","")
            genre=genre.replace("\n","")
            genre=genre.replace(">","=")
            genre=genre.split('=')
            genre=genre[int(len(genre)/2)] 
            result_genres.append(genre)
    return result_genres

def check_repeated_comma(x):
    list_x=x.split(',')
    if len(list_x)==3:
        return x
    else:
        return np.nan

def data_set(url):
    data_set=pd.DataFrame(columns=["Movie","Primary Genre","Secondary Genre","Tertiary Genre"])
    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')
   # print(soup)
    title=get_all_titles(soup)
    #print(title)
    genres=get_all_genres(soup)
    print(genres)
    data_set["Movie"]=pd.Series(title)
    data_set["Primary Genre"]=pd.Series(genres)
    data_set["Primary Genre"]=data_set["Primary Genre"].apply(check_repeated_comma)
    data_set['Secondary Genre']=data_set['Secondary Genre'].fillna('To Be FIlled')
    data_set['Tertiary Genre']=data_set['Tertiary Genre'].fillna('To Be FIlled')
    data_set=data_set.loc[data_set['Primary Genre']!=np.NaN]
    data_set=data_set.dropna(how="any")
    data_set[["Primary Genre","Secondary Genre","Tertiary Genre"]]=data_set["Primary Genre"].str.split(',',expand=True)
    data_set.to_csv("Dataset1.csv",mode='a',header=False)
    print(data_set)
print("IMDB scrapper")
number_of_pages=int(input("Enter the number of pages to be scraped: "))
for i in range(number_of_pages) :
    url=input('Enter the url:')
    data_set(url)







