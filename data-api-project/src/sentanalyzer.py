from pymongo import MongoClient
from src.config import DBURL
import pandas as pd
from bson.json_util import dumps
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean, pdist, squareform

from src.app import app
from src.user import *
from src.errorHand import errorHandler, Error404

#---------------------------------------------------------------

sia = SentimentIntensityAnalyzer()

# User sentiment
def sentUser(nameid):
    usquotes = list(db_quotes.find({"user": f"{nameid}"},{"_id":0, "quote":1}))
    #usernames = list(db_quotes.distinct("user"))
    return {"name": nameid,"Sent Socres": sia.polarity_scores(str(usquotes).strip('[]'))}

# Chat sentiment
def sentChat(chat_id):
    chatids = list(db_quotes.distinct("chat_id"))
    if int(chat_id) in chatids:
        chatquotes = list(db_quotes.find({"chat_id": int(chat_id)},{"_id":0, "quote":1}))
        sentscores = sia.polarity_scores(str(chatquotes).strip('[]'))
        return ({"The sentiment in this conversation is": dumps(sentscores)})
    else:
        return {f"Sorry, the chat {chat_id} does not exist. The vailable chats are": dumps(chatids)}

    return sentscores

# All users sentiment
def recUser(nam):
    usnames = (db_quotes.distinct("user"))
    if nam in usnames:
        usernames = list(db_quotes.distinct("user"))
        dicc = []
        for e in usernames:
            quotes = list(db_quotes.find({"user": e },{"_id":0, "quote":1}))
            sentscores = sia.polarity_scores(str(quotes).strip('[]'))
            dicc.append({"User": e, "neg": sentscores['neg'],  "neu": sentscores['neu'], "pos": sentscores['pos']})
        
        dt = pd.DataFrame.from_dict(dicc).set_index('User').T
        dist = pd.DataFrame(1/(1+ squareform(pdist(dt.T, 'euclidean'))), index=dt.columns, columns=dt.columns)
        sim = dist[nam].sort_values(ascending=False)[1:4].index
        return {f"The users that have more in commun with {nam} are": dumps(sim)}
    else:
        return ({f"Sorry, this User does not exists"})