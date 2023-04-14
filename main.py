import requests
import json
from fastapi import FastAPI
app = FastAPI()
import pymongo
from bson.json_util import dumps
from datetime import date
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import datetime


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["appUser"]
collection = db["user"]

myUser = {"name": "marco", "cognome": "campanale", "dataNascita": "07-12-2002", "maggiorenne": True}
#x = collection.insert_one(myUser)
print(myUser)

data = datetime.datetime
print( data)

@app.get("/getUser")
def get_User(name: str = None, cognome : str = None):
    if name == None and cognome == None:
        record = collection.find()
        list_record = list(record)
        json_data = dumps(list_record)
        dataInserimento = str(datetime.datetime.now())
        return {"response": json_data , "dataInserimento": dataInserimento}
    else:
        recordName = collection.find({"name": name})
        recordCognome = collection.find({"cognome": cognome})
        responseALL = collection.find({"name": name, "cognome": cognome})
        listRecordName = list(recordName)
        listRecordCognome = list(recordCognome)
        listResponseAll = list(responseALL)
        json_data_name = dumps(listRecordName)
        json_data_cognome = dumps(listRecordCognome)
        json_response_all = dumps(listResponseAll)
        jsonResponseQueryNome =  {"data": json_data_name}
        jsonResponseQueryCognome = {"dataCognome": json_data_cognome}
        if json_data_name:
            return jsonResponseQueryNome
        elif recordCognome:
            return jsonResponseQueryCognome
        else:
            return json_response_all
            




@app.post("/addUser")
def add_user(name: str, cognome: str, dataNascita : datetime.datetime):
    currentDate  = datetime.datetime.today().year
    eta = currentDate - dataNascita.year
    if eta >=  18: 
        maggiorenne = True
    else:
        maggiorenne = False    
    queryAdd = {"name":name, "cognome": cognome, "dataNascita": dataNascita,"dataInserimento" : datetime.datetime.now(), "maggiorenne": maggiorenne}
    print(queryAdd)
    addRecord = collection.insert_one(queryAdd)
    id = str(addRecord.inserted_id)
    dataInserimento = str(datetime.datetime.now())
    json_compatible_item_data = {"id" : jsonable_encoder(id), "dataInserimento": dataInserimento }
    return JSONResponse(content=json_compatible_item_data) 
