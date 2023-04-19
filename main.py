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
from functools import reduce
from operator import mul
import numpy as np

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["appUser"]
collection = db["user"]

myUser = {"name": "marco", "cognome": "campanale", "dataNascita": "07-12-2002", "maggiorenne": True}
#x = collection.insert_one(myUser)
print(myUser)

data = datetime.datetime


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

#punto 1
@app.get("/numCheck")
def controlNumber(num : float):
    if num >= 0:
        return {"positivo": num}
    else :
        return {"negativo": num}
    
#punto2
@app.get("/onlySum")
def onlySum(n1 : int, n2 : int):
  list1 = [n1, n2]
  result = reduce(mul, list1)
  print(result)
  return {"response": result}
    
#punto 3
@app.get("/numMax")
def numberMax(num1: int, num2:int, num3:int):
        listNumber = [num1, num2, num3]
        listNumber.sort()
        print(listNumber)
        return {"maxValue": listNumber[-1]}
    
#punto 4
@app.get("/areaTriangolo")
def areaTriangolo(b:int, h: int):
    area = (b*h)/2
    return {"areaTrangolo": area}

#punto 5
@app.get("/numMax2")
def numMax2(n1:int, n2:int):
    numbers = [n1, n2]
    return {"maxValue": max(numbers)}


@app.get("/sommaArray")
def sommaArray(n1:int):
    list = range(0,n1)
    print(list)
    if list < 0:
        resultN = sum(list)
        return {"responseNegative": resultN}
    else:
        result = sum(list)
        return {"responsePositive": result}



@app.get("/media")
def media(n1:int, n2:int, n3:int, n4:int):
    m = (n1+n2+n3+n4)/4
    return {"media": m}

@app.get("/sconto")
def sconto(n:int):
    if n >= 300:
        s = (n * 5)/100
        prezzoFinale = n - s
        return {"prezzo scontato" : prezzoFinale}
    else:
        return {"prezzo non scontato": n}

@app.get("/pagamento")
def pagamento(n:float, prezzoProdotto: float):
    resto = n - prezzoProdotto
    if resto >= 200:
        banconotaResto = (n-prezzoProdotto)/200
        return {"banconote": banconotaResto ,"banconota":  "da 200 euro"}
    elif resto >= 100:
        banconotaResto = (n-prezzoProdotto)/100
        return {"test": banconotaResto , "banconota": "da 100 euro"}
    elif resto >= 50:
        banconotaResto = (n-prezzoProdotto)/50
        return {"banconote": banconotaResto, "banconota": "da 50 euro"}
    elif resto >= 20:
        banconotaResto = (n-prezzoProdotto)/20
        return {"banconote": banconotaResto ,"banconota": "da 20 euro"}
    elif resto >= 10:
        banconotaResto = (n-prezzoProdotto)/10
        return {"banconote": banconotaResto ,"banconota":  "da 10 euro"}
    elif resto >= 2 and resto <=3:
        banconotaResto = (n-prezzoProdotto)/2
        banconotaResto2 = int(banconotaResto) + 1
        print(banconotaResto)
        if banconotaResto >= 1.5:
            banconota = "da 2 euro e 1 euro"
        else :
            banconotaResto2 = banconotaResto
            banconota = "da 2 euro"
        return {"banconote": banconotaResto2,  "banconota":  banconota}

    elif resto >= 1:
        banconotaResto = (n-prezzoProdotto)/1
        return {"banconote": banconotaResto,"banconota":  "da 1 euro"}

