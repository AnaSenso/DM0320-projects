from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
import re

from src.app import *
from src.errorHand import *

#---------------------------------------------------------------

# (GET) /chat/<chat_id>/adduser
#   - **Purpose:** Add a user to a chat, this is optional just in case you want to add more users to a chat after it's creation.
#   - **Params:** `user_id`
#   - **Returns:** `chat_id`


client = MongoClient(DBURL)
print(f"Connected to {DBURL}")
db_quotes = client.get_default_database()["quotes"]

def listChat(chatid):
    chatids = list(db_quotes.distinct("chat_id"))
    if int(chatid) in chatids:
        chatname = db_quotes.find_one({"chat_id":int(chatid)},{"_id":0,"chat":1})["chat"]
        chats = db_quotes.find({"chat_id":int(chatid)},{"_id":0,"chat":1, "user":1, "quote":1})
        return {f"This is the conversation of the chat {chatname}": dumps(chats)}
    else:
        return {f"Sorry, the chat {chatid} does not exist. The vailable chats are": dumps(chatids)}

def createChat():
    chatname = request.args.get("name")
    user = request.args.getlist("user")
    nchatid = max(db_quotes.distinct("chat_id"))+1
    chatnames = list(db_quotes.distinct("chat"))
    if chatname:
        if chatname in chatnames:
            return ({"Sorry, this chat already exist": dumps(chatname), "To create a new one": "choose another name" })
        else:
            if user:
                for e in user:
                    nuserid = max(db_quotes.distinct("user_id"))+1
                    nchat = {"user": e, "user_id": nuserid , "chat":chatname, "chat_id": nchatid}
                    db_quotes.insert_one(nchat)
            else:
                raise APIError("You must introduce query parameter ?user=<username>")
    else:
        raise APIError("You must introduce query parameter ?name=<chatname>")
    return ({"Yay!":"You have created a new chat", "Chat name": chatname, "With the users": user, "Chat ID": nchatid})

def createMessage(chat_id):
    userid = request.args.get("userid")
    #chid = request.args.get("chatid")
    message = request.args.get("mess")
    chids = db_quotes.distinct("chat_id")
    chatname = db_quotes.find_one({"chat_id":int(chat_id)}, {"_id":0, "chat":1})["chat"]
    usname = db_quotes.find_one({"user_id":int(userid)}, {"_id":0, "user":1})["user"]
    userchats = db_quotes.distinct("chat_id" ,{"user_id":int(userid)})
    if int(chat_id) in chids:
        if int(chat_id) in userchats:
            nmess = {"user": usname, "user_id": int(userid) , "quote": message ,"chat":chatname, "chat_id": int(chat_id)}
            db_quotes.insert_one(nmess)
            return ({f"You have introduced this message": dumps(nmess)})
        else:
            return ({f"Sorry, {usname} is not in this chat. {usname} is in chats": dumps(userchats)})
    else:
        return ({f"Sorry, this chat don't exist. The available chats are": dumps(chids)})
