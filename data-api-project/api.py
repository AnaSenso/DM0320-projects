from src.config import PORT
from flask import Flask, request

from src.app import app
from src.user import *
from src.chat import *
from src.sentanalyzer import *
from src.errorHand import *

# User endpoints
@app.route("/user/<name>")
@errorHandler
def getName(name):
    nombre = getUser(name)
    return nombre

@app.route("/user/create/<username>")
@errorHandler
def makeUser(username):
    newuser = createUser(username)
    return newuser

@app.route("/user/<nameid>/sentiment")
@errorHandler
def sentimentUser(nameid):
    sentus = sentUser(nameid)
    return sentus

#Sentiment recomendation
@app.route("/user/<nam>/recommend")
@errorHandler
def sentimentRecomm(nam):
    recuser = recUser(nam)
    return recuser

# Chat endpoints
@app.route("/chat/<chat_id>/sentiment")
@errorHandler
def sentimentChat(chat_id):
    senchat = sentChat(chat_id)
    return senchat

@app.route("/chat/<chat_id>/list")
@errorHandler
def allChats(chat_id):
    allchats = listChat(chat_id)
    return allchats

@app.route("/chat/create")
@errorHandler
def makeChat():
    makechat = createChat()
    return makechat

@app.route("/chat/<chat_id>/addmessage")
@errorHandler
def makeMess(chat_id):
    makemess = createMessage(chat_id)
    return makemess

app.run("0.0.0.0", PORT, debug=True)