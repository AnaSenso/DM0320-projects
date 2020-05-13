from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
import re

from src.app import app
from src.errorHand import errorHandler, Error404

#---------------------------------------------------------------

client = MongoClient(DBURL)
print(f"Connected to {DBURL}")
db_quotes = client.get_default_database()["quotes"]
db_users = client.get_default_database()["users"]

# (GET) /user/<user_id>/recommend
#   - **Purpose:** Recommend friend to this user based on chat contents
#   - **Returns:** json array with top 3 similar users
#{"_id":0, "user":1, "user_id":1, "chat":1}

def getUser(name):
    namereg = re.compile(f"^{name}", re.IGNORECASE)
    user = db_quotes.find_one({"user":namereg})["user"]
    userid = db_quotes.find_one({"user":namereg})["user_id"]
    userchat = db_quotes.distinct("chat" ,{"user":namereg})
    return {"Name": user, "User ID": userid, "Chat": userchat}

def createUser(username):
    #namereg = re.compile(f"^{username}", re.IGNORECASE)
    usernames = (db_quotes.distinct("user"))
    if username in usernames:
        userex = db_quotes.find_one({"user":username},{"user_id":1, "user":1})
        return {"Error":"This User already exists", "info":dumps(userex)}
    else:
        nuserid = max(db_quotes.distinct("user_id"))+1
        nuser = {"user":username, "user_id": int(nuserid)}
        db_quotes.insert_one(nuser)
        return {"Yay!":"You have created a new user", "info":dumps(nuser)}

