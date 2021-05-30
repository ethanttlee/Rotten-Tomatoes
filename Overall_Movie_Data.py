#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
import requests
import bs4
import time


# In[3]:


df = pd.read_csv('movies.csv')


# In[4]:


df['Movie Link'] = df['Movie Link'].str.strip('[]').str.split(',').apply(lambda x: ['http://www.' + i.strip().strip("''") for i in x])


# In[ ]:


my_dict = {'movie': [], 'release date': [], 'rating':[], 'genre':[],
          'language':[], 'directors':[], 'duration':[], 'Box Office':[],
          'Description': [], 'Audience Score':[], 'Tomatometer':[]}
for i in df['Movie Link']:
    for movie_url in i:
        url = movie_url
        time.sleep(15)
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text)
        movie = url.split('/')[-1]
        audience_score = soup.find('score-board')['audiencescore']
        tomatometer = soup.find('score-board')['tomatometerscore']
        description = soup.find('div', {'id':'movieSynopsis'}).text.strip('\n').strip()
        bs4_obj = soup.find('ul', {'class':'content-meta info'})
        #all_info = bs4_obj.find_all('div', {'data-qa':'movie-info-item-value'})
        if bs4_obj.find('div', {'class':'meta-value'}):
            rating = bs4_obj.find('div', {'class':'meta-value'}).text.strip()
        else:
            rating = np.NaN
        if bs4_obj.find('div', {'class':'meta-value genre'}):
            genre = bs4_obj.find('div', {'class':'meta-value genre'}).text
            cleaned_genre = re.findall('([a-zA-Z][^,]*)' ,genre.strip())
        else:
            cleaned_genre = np.NaN
        if len(bs4_obj.find_all('div', {'data-qa':'movie-info-item-value'})) >= 3:
            language = bs4_obj.find_all('div', {'data-qa':'movie-info-item-value'})[2].text.strip()
        else:
            language = np.NaN
        if bs4_obj.find('a', {'data-qa':'movie-info-director'}):
            directors = bs4_obj.find('a', {'data-qa':'movie-info-director'}).text
            cleaned_directors = re.findall('([\w]+ [\w]+)', directors)
        else:
            cleaned_directors = np.NaN
        if len(bs4_obj.find_all('time')) >= 1:
            release_date = bs4_obj.find_all('time')[0].text.strip()
        else:
            release_date = np.NaN
        if len([i.text for i in bs4_obj.find_all('div',{'class':"meta-value" , 'data-qa':"movie-info-item-value"}) if '$' in i.text]) == 0:
            box_office = np.NaN
        else:
            box_office = [i.text for i in bs4_obj.find_all('div',{'class':"meta-value" , 'data-qa':"movie-info-item-value"}) if '$' in i.text][0]
        if len(bs4_obj.find_all('time')) >= 2:
            duration = bs4_obj.find_all('time')[-1].text.strip()
        else:
            duration = np.NaN
        if not pd.isnull(rating):
            if re.findall('([a-zA-Z][^,]*)' ,rating.strip()) == cleaned_genre:
                rating = np.NaN
            elif re.findall('([\w]+ [\w]+)', rating) == cleaned_directors:
                rating = np.NaN
        my_dict['movie'].append(movie)
        my_dict['release date'].append(release_date)
        my_dict['rating'].append(rating)
        my_dict['genre'].append(cleaned_genre)
        my_dict['language'].append(language)
        my_dict['directors'].append(cleaned_directors)
        my_dict['duration'].append(duration)
        my_dict['Box Office'].append(box_office)
        my_dict['Description'].append(description)
        my_dict['Audience Score'].append(audience_score)
        my_dict['Tomatometer'].append(tomatometer)

