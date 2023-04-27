import csv
import pymongo 
import pandas as pd
import json
from csv import reader
from datetime import datetime


mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
csvFile = pd.read_csv('posWIMTres_HO.csv')
csvFile.head()
header = csvFile.columns
value = csvFile.values
jsonFile = csvFile.to_json()
data = csvFile.to_dict(orient="records")
db = mongoClient["dbCSV"]
lista = []
dataInserimento = {"dataInserimento":datetime.today()}
lista.append(dataInserimento)
with open("posWIMTres_HO.json") as file:
    file_data = json.load(file)
insert = db.csv.insert_many(file_data)
insertDate= db.csv.insert_many(lista)
