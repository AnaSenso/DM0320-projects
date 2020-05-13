import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import numpy as np
import requests
from pymongo import MongoClient
from datetime import date

# Get today's year
this_year = str(date.today())[0:4]

# Working with json and dataframes
def officeToGeoPoint(row):
    office = row.offices
    if type(office) == dict:
        if 'latitude' in office and 'longitude' in office:
            if(type(office["latitude"])) == float and type(office["longitude"]) == float:
                return ({
                    "type":"Point",
                    "coordinates":[office["longitude"],office["latitude"]]
                },"success")
            else:
                return(None,"Invalid lat lat and long")
        else:
            return (None,"No lat and long keys in office dict")
    return (None,"No office")

def officeToAddress(row):
    address = row.offices
    if type(address) == dict:
        if 'address1' in address and 'city' in address:
            return (address["address1"],address["city"])
        else:
            return (None,"No office")

def officeToLatLong(row):
    address = row.offices
    if type(address) == dict:
        if 'latitude' in address and 'longitude' in address:
            lat = str(address["latitude"])
            longt = str(address["longitude"])
            return f"{lat},{longt}"
        else:
            return (None,"No lat and long")

def getOfficeNear(address, maxDist=2000):
    point = geocode(address)
    return {
       "office": {
         "$near": {
           "$geometry": point,
           "$maxDistance": maxDist,
         }
       }
    }

# Fordward geocoding
def geocode(address):
    res = requests.get(f"https://geocode.xyz/{address}",params={"json":1})
    data = res.json()
    print(res)
    return {"type":"Point",
        "coordinates": [float(data["longt"]), float(data["latt"])]}

def pointNear(poin, maxDist=2000):
    return {
       "office": {
         "$near": {
           "$geometry": poin,
           "$maxDistance": maxDist,
         }
       }
    }

def ckeck2km(db, addresses, name):
    cur = db.find(addresses,{"name":1,"geopoint":1, "address":1, "city":1})
    if len(list(cur))>0:
        return f"there are {name} companies near by {addresses}: {list(cur)}"
    else:
        return f"there are NO {name} near by"


apiKey = os.getenv("MAPSAPI")

# Get info from Maps API
def getSearch(location, distance, place):
    path = '/place/nearbysearch/json'
    url=f"https://maps.googleapis.com/maps/api{path}"
    headers = {"Authorization":f"token {apiKey}"} if apiKey else {}
    queryParams = {
        "location": location,
        "radius": f"{distance}",
        "keyword": f"{place}",
        "fields": "formatted_address,name,geometry,type",
        "key": apiKey}
    res = requests.get(url, params=queryParams, headers=headers)
    return res.json()

def checkNear(df,distance, place):
    noplace = []
    places = []
    for i,e in df.iterrows():
        get = getSearch(df['geocoord'][i],distance,place)
        if get['status'] == 'OK':
            places.append(df['name'][i])
        else:
            noplace.append(df['name'][i])
    print(f"This companies do has a {place} near by: {places}")
    print(f"This companies does NOT has a {place} near by: {noplace}")
    return df[~df['name'].isin(noplace)]

def getMaps(address,input):
    path= "/place/findplacefromtext/json"
    url=f"https://maps.googleapis.com/maps/api{path}"
    headers = {"Authorization":f"token {apiKey}"} if apiKey else {}
    queryParams = {
        "input": f"{input} near {address}",
        "inputtype":"textquery",
        "fields": "name,formatted_address,geometry",
        "key": apiKey}
    res = requests.get(url, params=queryParams, headers=headers)
    return res.json()

def getPlaces(df, place):
    places = []
    for i,e in df.iterrows():
        getM = getMaps((df['address'][i],df['city'][i]),place)
        if getM['status'] == 'OK':
            places.append(getM)
    return places

def officeToLatLong(row):
    address = row.offices
    if type(address) == dict:
        if 'latitude' in address and 'longitude' in address:
            lat = str(address["latitude"])
            longt = str(address["longitude"])
            return f"{lat},{longt}"
        else:
            return (None,"No lat and long")

#findplace= "/place/findplacefromtext/json"
#autocomp = "/place/autocomplete/json"
#search = "/place/nearbysearch/json"
