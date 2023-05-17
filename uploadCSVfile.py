import csv
import pymongo 
import pandas as pd
import json
from csv import reader
from datetime import datetime
import bson

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
csvFile = pd.read_csv('posWIMTres_HO.csv')
jsonFile = csvFile.to_json()
data = csvFile.to_dict(orient="records")
db = mongoClient["dbCSV"]
with open("posWIMTres_HO.json") as file:
    file_data = json.load(file)
    dataInserimento = str(datetime.today())
    jsonData = dataInserimento
file_data[-1] = {"dataInserimeto":jsonData}
#insert = db.csv.insert_many(file_data)
import csv 
import json 

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 

        for row in csvReader: 
            jsonArray.append(row)
  
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)
          
csvFilePath = r'posWIMTres_HO.csv'
jsonFilePath = r'data.json'
print(jsonFilePath)
csv_to_json(csvFilePath, jsonFilePath)
