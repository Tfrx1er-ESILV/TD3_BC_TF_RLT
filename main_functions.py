import csv , os
import requests
import json
import time , datetime
os.system("clear")

#Lecture du fichier log_id
#Renvoie un tab de deux string [0] = id , [1] = pwd
def import_log():
    log = []
    with open('log_id.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            log.append(row[0])
            log.append(row[1])
    
    return [log[2],log[3]]   

#Renvoie tout les couples tradé sur Coinbase pro
#Renvoie un tab de string
def get_all_products():
    _return = []
    data = requests.get("https://api.pro.coinbase.com/products").json()
    for element in data:
        if not element['base_currency'] in _return:
            _return.append(element['base_currency'])
    return _return

#Renvoie tout les id sous forme de tab de string
#Renvoie tout les id sous forme de tab de string
def get_all_products_id():
    _return = []
    data = requests.get("https://api.pro.coinbase.com/products").json()
    for element in data:
        _return.append(element['id'])
    return _return

#Renvoie le bid ou le ask en float
#Exemple :
#name = "ETH-EUR"  direction = "asks" ou "bids"
def get_bid_ask_product(name,direction):
    _return = []
    data = requests.get("https://api.pro.coinbase.com/products/"+name+"/book").json()
    data = float(data[direction][0][0])
    return data

#Renvoie la sequence, le bid et ask pour un couple donné
#Exemple :
#name = "ETH-EUR"
def export_order_book(name):
    data = requests.get("https://api.pro.coinbase.com//products/"+name+"/book").json()
    return data

#Prend un epoch time et le converti en ISO8601
def convertEpochIso8601(time) : 
    dt = datetime.datetime.utcfromtimestamp(time)
    iso_format = dt.isoformat() + 'Z'
    return iso_format

#Renvoie le time, low, high, open, close, volume 
#d'une chandelle (historic rates of an asset)
#Exemple : name = "ETH-EUR", duration = "300"
def refresh_Data_Candles(name,duration):
    return requests.get("https://api.pro.coinbase.com/products/"+name+"/candles?granularity="+duration).json()

#Renvoie une candle une tranche de 10 jours de candle
first_date_computable = 1451606400

#Renvoie une candle une tranche de 10 jours de candle
first_date_computable = 1451606400

def obtain_data_candle(name,time,duration):
    start = convertEpochIso8601(time)
    end = convertEpochIso8601(time + 10*24*3600 - 1)
    response = requests.get("https://api.pro.coinbase.com/products/"+name+"/candles?start="+start+"&end="+end+"&granularity="+str(duration)).json()
    return response

def obtain_one_candle(name,time,duration):
    start = convertEpochIso8601(time)
    end = convertEpochIso8601(time +100)
    response = requests.get("https://api.pro.coinbase.com/products/"+name+"/candles?start="+start+"&end="+end+"&granularity="+str(duration)).json()
    return response[0]