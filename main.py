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

data = datetime.datetime.now()
print( data)

@app.get("/getUser")
def get_User():
    record = collection.find()
    list_record = list(record)
    json_data = dumps(list_record)
    dataInserimento = str(datetime.datetime.now())
    return {"response": json_data , "dataInserimento": dataInserimento}
    


@app.post("/addUser")
def add_user(name: str, cognome: str, dataNascita : str , maggiorenne : bool):
    queryAdd = {"name":name, "cognome": cognome, "dataNascita": dataNascita, "maggiorenne":maggiorenne,"dataInserimento" : datetime.datetime.now()}
    addRecord = collection.insert_one(queryAdd)
    print(collection.count_documents({}))
    print(addRecord.inserted_id)
    id = str(addRecord.inserted_id)
    dataInserimento = str(datetime.datetime.now())
    json_compatible_item_data = {"id" : jsonable_encoder(id), "dataInserimetno": dataInserimento}
    print(json_compatible_item_data)
    return JSONResponse(content=json_compatible_item_data) 

