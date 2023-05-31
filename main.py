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
import random
import numpy
import numpy as np
import math
import csv
from fastapi.encoders import jsonable_encoder
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["appUser"]
collection = db["user"]

myUser = {"name": "marco", "cognome": "campanale", "dataNascita": "07-12-2002", "maggiorenne": True}
#x = collection.insert_one(myUser)

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
    start = 0
    end = n1
    list = range(start, end)
    sorted(list)
    print(sorted(list))
    if n1 > 0:
        result = sum(list)
        return {"responsePositive": result}
    else:
        start = n1
        end = 0
        list = range(start,end)
        sorted(list)
        print(list)
        resultN = sum(list) - start
        return {"responseNegative": resultN}
       



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
        return {"banconote": banconotaResto ,"banconotaRicevente":  "da 200 euro"}
    elif resto >= 100:
        banconotaResto = (n-prezzoProdotto)/100
        return {"test": banconotaResto , "banconotaRicevente": "da 100 euro"}
    elif resto >= 50:
        banconotaResto = (n-prezzoProdotto)/50
        return {"banconote": banconotaResto, "banconotaRicevente": "da 50 euro"}
    elif resto >= 20:
        banconotaResto = (n-prezzoProdotto)/20
        return {"banconote": banconotaResto ,"banconotaRicevente": "da 20 euro"}
    elif resto >= 10 and resto < 20:
        banconotaResto = (n-prezzoProdotto)/10
        restoRimanente = resto - 10
        output = "da 10€" + " "+"e da "+" "+ str(restoRimanente)+"€" 
        if resto >= 11 and resto < 15:
            restoRimanente = resto - 10
            output = "da 10€" + " "+"e da "+" "+ str(restoRimanente)+"€" 
        if resto == 15:
            restoRimanente = 1
        elif resto > 15 and resto <= 16:
            restoRimanente = 2 
            output = "da 10€"+ " "+"e da "+" "+ "5.0 e 1.0€"
        elif resto == 17:
            restoRimanente = 2
            output = "da 10€"+ " "+"e da "+" "+ "5.0 e 2.0€"
        elif resto == 18:
            restoRimanente = 3
            output = "da 10€"+ " "+"e da "+" "+ "5.0 e 2.0€ e 1.0€"
        return {"banconote": 1 ,"banconota2":restoRimanente,"banconotaRicevente":  output}
    elif resto >= 5 and resto <=9:
        banconotaResto = (n-prezzoProdotto)/5
        print(banconotaResto)
        restoRimanente = resto - 5
        output = "da 5€" + " "+"e da "+" "+ str(restoRimanente)+"€"
        print(output) 
        if restoRimanente >= 3 and restoRimanente<5:
            if restoRimanente == 3:
                restoRimanente = 2
                output = "da 5€" + " "+"e da "+"2.0€ e 1.0€ "
            else :
                restoRimanente = 2
                output = "da 5€" + " "+"e da "+"2.0€ e 2.0€ "
        return {"banconota1": 1,"banconota2":restoRimanente ,"banconotaRicevente": output}
    elif resto == 4:
        banconotaResto = (n-prezzoProdotto)/2
        output = "da 2€"
        return {"banconota": banconotaResto, "banconotaRicevente": output}
    elif resto >= 2 and resto <=3:
        banconotaResto = (n-prezzoProdotto)/2
        banconotaResto2 = int(banconotaResto) + 1
        if banconotaResto >= 1.5:
            banconota = "da 2 euro e 1 euro"
        else :
            banconotaResto2 = banconotaResto
            banconota = "da 2 euro"
        return {"banconote": banconotaResto2,  "banconotaRicevente":  banconota}

    elif resto >= 1 and resto < 2:
        banconotaResto = (n-prezzoProdotto)/1
        return {"banconote": banconotaResto,"banconota":  "da 1 euro"}
   
    
@app.delete("/deleteUser")
def deleteUSer(id):
    myquery = {"_id": id}
    collection.delete_one(myquery)
    return {"user eliminato": myquery}

@app.put("/updateUser")
def updateUser(id):
    myquery = {"cognome": "campanale"}
    queryUpdate = {"$set":{"cognome": "campa"}}
    collection.update_one(myquery,queryUpdate)
    return {"dato aggiornato": queryUpdate}

@app.get("/numberRandom")
def numberRandom(p1:int, p2:int):
    if p2 <=10 and p1 <=10:
        p1 = random.randint(1,10)
        p2 = random.randrange(1,10)
        n = random.randrange(1,p2)
        element = []
        result = []
        key = 1
        while key <= p2:
            key += 1
            value = []
            for n in range(p1):
                n = random.randint(1,10)
                print(n)
                json_responseValue =n
                value.append({"value":json_responseValue})
                valueObject = random.randint(0,n)
                for n  in value:
                    valueObject = value
                    valueFinal= valueObject
                    print(valueFinal)
            keyString = "element" + str(key -1)
            element.append({keyString:valueFinal})
        #print(element)
            result =({"response": element, "p1Rand":p1, "p2Rand":p2})
        return result
    else:
        if p1 >= 10 and p2 >= 10:
            return {"error": "paramentri devono essere minori di 10"}
        if p1 >= 10:
            return {"error": "iL paramentro p1 deve essere minore di 10"}
        elif p2 >= 10:
            return {"error": "iL paramentro p2 deve essere minore di 10"}



@app.get("/getArrayReverse")
def arrayReverse(n:int):
    randomlist = []
    for i in range(n):
        numberRandom = random.randint(1,30)
        numberRandom2 = random.randint(1,10)
        result = (numberRandom/numberRandom2)*2 
        result = int(result)          
        if (result % 2) == 0:
           randomlist.append(+result)
        else:
            randomlist.append(-result)
        listReverse = [result for result in randomlist if result >= 0][::-1]
    if result:
        return {"arrayIniziale": randomlist, "arrayFinale": listReverse}
    else:
        return {"error":"error"}

@app.get("/multipliDiTre")
def multipliDiTre(n:int):
    list = []
    for i in range(int(n)):
        print("Enter number at index", i, )
        item = int(input())
        list.append(item)
        print("User list is ", list)
        listMultiplo = []
        for x in list:
            if(int(x) % 3) ==0:
                print (x)
                listMultiplo.append(x)
                print(listMultiplo)
                media =  numpy.mean(listMultiplo)
    return {"list":list,"mediaMultipli3": media}

@app.get("/reverseArray")
def reverseArray(n:int):
    if n >= 6:
        lista = []
        for x in range(n):
            finalList = []
            valueArray = random.randint(1,10)
            lista.append(valueArray)
            for i in lista:
                lista1 = lista[0]
                lista2 = lista[-1]
            print(lista)
        print(lista[-2])
        if n == 6:
            finalList = lista1, lista2, lista[1], lista[-2],lista[2],lista[-3]
        elif n==7:
            finalList = lista1, lista2, lista[1], lista[-2],lista[2],lista[-3],lista[3]
        elif n == 8:
            finalList = lista1, lista2, lista[1], lista[-2],lista[2],lista[-3], lista [3], lista[-4]
        elif n == 10:
            finalList = lista1, lista2, lista[1], lista[-2],lista[2],lista[-3], lista [3], lista[-4], lista[4], lista[-5]
        elif n == 16:
            finalList = lista1, lista2, lista[1], lista[-2],lista[2],lista[-3], lista [3], lista[-4], lista[4], lista[-5],lista[5],lista[-6],lista[6],lista[-7],lista[7],lista[-8]

        print(finalList)
        return {"lista":lista, "listaFinale": finalList}
    else:
        print("error")



@app.get("/sumElementArray")
def sumElementArray(n:int):
    lista = []
    sumList = 0
    sumOddList = 0
    if n >= 6 :
        for x in range(n):
            valueArray = random.randint(1,10)
            lista.append(valueArray)
            print(lista)
        for i in range(0, len(lista), 2):
            sumList += (lista[i])
            print(sumList)
        for y in range(1,len(lista)):
            if y% 2 != 0:
                sumOddList +=(lista[y])
                print(sumOddList)
            else: 
                print("errp")
        if sumList == sumOddList:
            sameResult = True
        else:
            sameResult = False
            return {"lista": lista, "sommaPari": sumList, "sommaDispari":sumOddList,"risultatoUguale": sameResult}          
    elif n < 6:
        return {"error, parametro inferiore a 6":n }
    


@app.get("/fattoriale")
def fattoriale(n:int):
    i=1
    for y in range(1, n+1):
        i*=y
        print(i)
    return {"numero":i}


@app.get("/areaTrapezi")
def areaTrapezi(a1:int,b1:int,h1:int,a2:int,b2:int,h2:int):
    if a1 > 0 and b1 > 0 and h1 >0 and a2 > 0 and b2 >0 and h2 >0: 
        area1 = ((a1+b1)*h1)/2
        area2 = ((a2+b2)*h2)/2
        if area1 > area2:
            areamaggiore = area1
        else:
            areamaggiore = area2
        return {"area1": area1, "area2":area2,"aereaMaggiore":areamaggiore}
    else :
        return {"errror, i paramentri di input devono essere maggiori di 0"}

@app.get("/triangolo")
def triangolo(l1:int,l2:int,l3:int):
    p = l1 +l2 +l3
    area = p/2 *((p/2)-l1)*((p/2)-l2)*((p/2)-l3)
    result = math.sqrt(area)
    
    return {"perimetro": p , "area": result}


@app.get("/annoBisestile")
def annoBisestile(n:int):
    if n%4 == 0 and n%100 != 0 or n%400 == 0:
        return {"annoBisestile":n, "verifica": True}
    else:
        return {"annoNonBisestile":n, "verfica":False}
    

@app.get("/returnMaxValue")
def returnMaxValue(n:int):
    lista= []
    if n > 4 and n < 100:
        for i in range(n):
            elementArray= random.randint(n,100)
            lista.append(elementArray)
            maxValue = max(lista)
        return {"lista": lista, "maxValue": maxValue}
    else:
        return {"error , messaggio di warning"}


@app.get("/returnJSON")
def returnJson():
    with open ("posWIMTres_HO.json") as file:
        data = json.load(file)
    return(data)

origins = [
   "http://localhost:8000","http://localhost:4200"
]
app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)



from bson import Binary, Code, ObjectId
from bson.json_util import dumps

@app.get("/returnCollection")
def returnCollection():
    mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
    db = mongoClient["dvCSV"]
    cursor = db['csv'].find()
    data = []
    for doc in cursor:
        doc['_id'] = str(doc['_id']) 
        data.append(doc)
    return data

@app.get("/data/{id}")
def getId(id:str):
    print("chiamata alla get id" + " " + id )
    mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
    db = mongoClient["dvCSV"]
    cursor = db['csv'].find({'_id':ObjectId(id)})
    data = []
    for doc in cursor:
        doc['_id'] = str(doc['_id']) 
        data.append(doc)
    print("contenuto di data ")
    print(data)
    return data

class UploadData(BaseModel):
    _id:ObjectId
    Entity: str
    Isin:str
    InstrumentName:str
    MaturityDate:str
    IssuerName:str
    IssuerCode:str
    Currency:str
    MarketCode:str
    AgentName:str
    SettledQty:str
    LatestCleanPrice:str
    LatestDirtyPrice:str
    PriceSource:str
    SettledValue:str
    BVALScore:str
    EligibileBCE:str
    EligibileFED:str
    EligibileHKM:str
    EligibileBOE:str
    Marketability:str
    LiquidityClass:str
    LiquidityClassHaircut:str
    LiquidityClassStressHaircut:str
    LiquidityClassPolicyHaircut:str
    LiquidityTypeName:str
    SecurityTypeName:str
    BBGLiquidityClassDate:str
    BBGLiquidityClass:str
    LRSNarrative:str
    BloombergCode:str

print(UploadData)

@app.post("/updateData/{id}")
def updateData(data:UploadData,id:str):
    print("inizio metodo updateData")
    mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
    db = mongoClient["dvCSV"]
    col = db["csv"]
    lista = []
    idObject = db['csv'].find({'_id':ObjectId(id)})
    for doc in idObject:
        doc['_id'] = str(doc['_id']) 
        lista.append(doc)
    lista = dict(data)
    filter = { '_id': ObjectId(id) }
    print(filter)
    newvalues = { "$set": lista  }
    print(newvalues)
    print("fine metodo updateData")
    insert = col.update_one(filter, newvalues)
    return {"result":insert.upserted_id}

@app.post("/insertData")
def insertData(data:UploadData):
    mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
    db = mongoClient["dvCSV"]
    col = db["csv"]
    col.insert_one(dict(data))
    return {"dato inserito": data}

from bson import ObjectId


@app.delete("/deleteData/{id}")
def deleteData(id:str):
    mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
    db = mongoClient["dvCSV"]
    col = db["csv"]
    idObject = db['csv'].find({'_id':ObjectId(id)})
    for doc in idObject:
        col.delete_one(doc)
    
    return {"user eliminato": doc}
       
