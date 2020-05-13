import pandas as pd
import os
from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
import numpy as np
import requests
import sys
from argparse import ArgumentParser
import subprocess

df = pd.read_csv('../input/tv_shows_final.csv')
df = df.drop(columns=['Unnamed: 0'])

def parse():
    parser=ArgumentParser(description="This program returns the best TV shows depending on the genre and a mimnum imdb rating choosen")
    parser.add_argument("--genre",dest="genre",type=str,help="The available genres are the following:'Documentary', 'Animation', 'Thriller','War', 'Comedy', 'Crime', 'Drama', 'Action', 'Fantasy', 'Western','Family', 'Romance', 'Biography', 'History', 'Mystery', 'Sport','Sci-Fi', 'Adventure', 'Horror'")
    parser.add_argument("--rating",dest="rating",type=float,help="Choose a minum rating. This is based on the imdb clasification")
    return parser.parse_args()

def tvshows(genre,rating):
    gen_df = df.loc[df[genre]>0]
    rat_df = gen_df.loc[df['imdbRating'] >= rating]
    tot = rat_df.iloc[:,[0,1,2,3,4,5,6,7]]
    days = int(tot['Hours'].mean()//12)
    hours = int(round(tot['Hours'].mean()%12))
    new = tot.iloc[:,[0,1,2,3,4,5,6]]
    plo = new.plot.bar('Title',"imdbRating")
    if new.empty == True:
        return ('Wow! You have high standards. Try to chose a lower rating')
    else:
        return f"Here is your selection, when and were you can watch them \n {new} \n You may spend an average of {days} days and {hours} hours witching each of them"

def main():
    args = parse()
    genre=args.genre
    rating=args.rating
    try:
        print(tvshows(genre,rating))
    except Exception:
        print('You must choose a valide genre and rating. For more info try main.py -h')

if __name__ == "__main__":
    main()
