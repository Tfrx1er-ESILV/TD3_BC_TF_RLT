import csv , os
import requests
import json
import time , datetime
os.system("clear")
import sqlite3
import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase


#Lecture du fichier log_id
def import_log():
    with open('log_id.json') as json_data:
        data_dict = json.load(json_data)
        return data_dict

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
    
#Prend une date en format ISO8601
def ISO_to_Epoch(date):
    ref = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    epoch_time = int((ref - datetime.datetime(1970, 1, 1)).total_seconds())
    return epoch_time
#Renvoie le time, low, high, open, close, volume 
#d'une chandelle (historic rates of an asset)
#Exemple : name = "ETH-EUR", duration = "300"
def refresh_Data_Candles(name,duration):
    return requests.get("https://api.pro.coinbase.com/products/"+name+"/candles?granularity="+duration).json()

#Renvoie une candle une tranche de 10 jours de candle
first_date_computable = 1451606400

#Récupère les information de candles sur 10 jours
def obtain_data_candle(name,time,duration):
    start = convertEpochIso8601(time)
    end = convertEpochIso8601(time + 10*24*3600 - 1)
    response = requests.get("https://api.pro.coinbase.com/products/"+name+"/candles?start="+start+"&end="+end+"&granularity="+str(duration)).json()
    return response

#Récupère les candles manquante en cherchant à la minute:30 près
def obtain_one_candle(name,time,duration):
    start = convertEpochIso8601(time)
    end = convertEpochIso8601(time +100)
    response = requests.get("https://api.pro.coinbase.com/products/"+name+"/candles?start="+start+"&end="+end+"&granularity="+str(duration)).json()
    return response[0]

def verifier_integriter_bd(name,max):
    connexion = sqlite3.connect(name)
    connexion = sqlite3.connect("basededonnees.db")
    liste_trou = []
    curseur = connexion.cursor()  #Récupération d'un curseur
    for id in range(max+1):
        curseur.execute("select * from Coinbase_BTC_EUR_3600 where id = "+str(id)+";")
        element = curseur.fetchone()
        if element == None:
            liste_trou.append(id)
    connexion.close()
    return liste_trou

#Extrait la dernière date de récupération des candles
def get_last_date(database_file):
    query = "SELECT max(date) FROM Coinbase_BTC_EUR_3600;"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results[0][0]


# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

api_url = 'https://api.pro.coinbase.com/'
auth = CoinbaseExchangeAuth(import_log()['log'], import_log()['secret'], import_log()['passphrase'])

# Get accounts
r = requests.get(api_url + 'accounts', auth=auth)
print(r.json())
# [{"id": "a1b2c3d4", "balance":...
