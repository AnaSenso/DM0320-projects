import pandas as pd
import os
from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
import numpy as np
import requests

df = pd.read_csv('../input/tv_shows_full.csv')
df = df.drop(columns=['Unnamed: 0'])
df = df.fillna('??')

order = ['Title', 'imdbRating', 'Plot', 'Genre','Day', 'Time', 'Network', 'Hours','Runtime in minutes',
       'imdbVotes', 'totalSeasons', 'Documentary', 'Animation', 'Thriller',
       'War', 'Comedy', 'Crime', 'Drama', 'Action', 'Fantasy', 'Western',
       'Family', 'Romance', 'Biography', 'History', 'Mystery', 'Sport',
       'Sci-Fi', 'Adventure', 'Horror', 'Episodes']
df_final = df.reindex(columns=order)

df_final.to_csv('../input/tv_shows_final.csv')

#print(df_final)

# def gen_fill(df, genre, col):
#     for gen in genre:
#         genre_lis = []
#         for e in list(df[col]):
#             if gen in e:
#                 genre_lis.append(e)
#             else:
#                 pass
#         df[gen] = np.where(df[col].isin(genre_lis), 1, 0)

# def get_show(title):
#     url = f"http://api.tvmaze.com/search/shows?q={title}"
#     res = requests.get(url)
#     return res.json()

# def fill_data(df):
#     show_day = [get_show(tit)[0]['show']['schedule']['days'] for tit in list(df['Title'])]
#     with_day = df.assign(Day = show_day)
#     show_time = [get_show(tit)[0]['show']['schedule']['time'] for tit in list(df['Title'])]
#     with_time = with_day.assign(Time = show_time)
#     show_net = []
#     for tit in list(df_shows['Title']):
#         try:
#             show_net.append(get_show(tit)[0]['show']['network']['name'])
#         except Exception:
#             show_net.append(get_show(tit)[0]['show']['webChannel']['name'])
#     with_day = with_time.assign(Network = show_net)
#     show_day = [get_show(tit)[0]['show']['schedule']['days'] for tit in list(df['Title'])]
#     with_everything = with_day.assign(Day = show_day)
#     return with_everything

# def get_epis(title):
#     url = f"http://api.tvmaze.com/search/shows?q={title}"
#     res = requests.get(url)
#     showid = res.json()[0]['show']['id']
#     ep = requests.get(f'http://api.tvmaze.com/shows/{showid}/episodes').json()
#     return len(ep)

# def time(df,col1, col2):
#     new_e = []
#     for e in range(len(df.index)):
#         new_e.append(round(((df.at[e,col1]*df.at[e,col2])/60),2))
#     new_df = df.assign(Hours= new_e)
#     return new_df