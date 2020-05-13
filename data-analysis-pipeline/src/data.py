from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import requests
from dotenv import load_dotenv
load_dotenv()

# Cleanning the data set
df = pd.read_csv('../input/tv_shows_ver2.csv')
df =  df.drop(columns=['Unnamed: 0','Director' , 'Writer','Type'])

df_shows = df.drop(columns=['Rated','Released' , 'Poster','Language', 'Country', 'Awards', 'Actors', 'Year', 'imdbID'])
order = ['Title','imdbRating', 'Plot','Genre', 'Runtime in minutes','imdbVotes', 'totalSeasons']
df_shows = df_shows.reindex(columns=order)

# Creating columns with Genre info
def gen_fill(df, genre, col):
    for gen in genre:
        genre_lis = []
        for e in list(df[col]):
            if gen in e:
                genre_lis.append(e)
            else:
                pass
        df[gen] = np.where(df[col].isin(genre_lis), 1, 0)

genres = set(map(str.strip, list(e for x in df['Genre'] for e in x.split(','))))
gen_fill(df_shows, genres, 'Genre')

titles = [e for e in df['Title']]

# Getting the API request
def get_show(title):
    url = f"http://api.tvmaze.com/search/shows?q={title}"
    res = requests.get(url)
    return res.json()

# Filling the dF with the number of episodes
def get_epis(title):
    url = f"http://api.tvmaze.com/search/shows?q={title}"
    res = requests.get(url)
    showid = res.json()[0]['show']['id']
    ep = requests.get(f'http://api.tvmaze.com/shows/{showid}/episodes').json()
    return len(ep)

# Filling the dF with the info about time day and network
def fill_data(df):
    show_day = [get_show(tit)[0]['show']['schedule']['days'] for tit in list(df['Title'])]
    with_day = df.assign(Day = show_day)
    show_time = [get_show(tit)[0]['show']['schedule']['time'] for tit in list(df['Title'])]
    with_time = with_day.assign(Time = show_time)
    show_net = []
    for tit in list(df_shows['Title']):
        try:
            show_net.append(get_show(tit)[0]['show']['network']['name'])
        except Exception:
            show_net.append(get_show(tit)[0]['show']['webChannel']['name'])
    with_day = with_time.assign(Network = show_net)
    show_day = [get_show(tit)[0]['show']['schedule']['days'] for tit in list(df['Title'])]
    with_everything = with_day.assign(Day = show_day)
    return with_everything

df_fill = fill_data(df_shows)
df_fill['Day'] = df_fill['Day'].str[0]

# Filling the data with the Hour info
epis = []
for tit in list(df_fill['Title']):
    epis.append(get_epis(tit))

df_full = df_fill.assign(Episodes = epis)
def time(df,col1, col2):
    new_e = []
    for e in range(len(df.index)):
        new_e.append(round(((df.at[e,col1]*df.at[e,col2])/60),2))
    new_df = df.assign(Hours= new_e)
    return new_df

df_final = time(df_full,'Runtime in minutes','Episodes')
df_final.to_csv('../input/tv_shows_full.csv')

#print(df_final)
#print(list(df_finall.columns))