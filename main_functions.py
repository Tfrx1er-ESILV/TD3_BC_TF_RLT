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
    ref = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%fZ')
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

def more_candles(j,start,end):
    connexion = sqlite3.connect("basededonnees.db")
    start_epoch = ISO_to_Epoch(start)
    #end_epoch = ISO_to_Epoch(end)
    for i in range(0,j): #0,149
        start = convertEpochIso8601(start_epoch + i * 10*24*3600) #10 jours
        end = convertEpochIso8601(start_epoch + i*10*24*3600)
        data = requests.get("https://api.pro.coinbase.com/products/BTC-EUR/candles?start="+start+"&end="+end+"&granularity=3600").json()
        print(data)
        for t in range(0,len(data)): #max == 237 
            query = "SELECT max(Id) FROM Coinbase_BTC_EUR_3600;"
            connection = sqlite3.connect("basededonnees.db")
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            maxi = results[0][0]
            _id = t+ int(maxi)

            _date = str(data[t][0])
            _high = data[t][2]
            _low = data[t][1]
            _open = data[t][3]
            _close = data[t][4]
            _volume = data[t][5]
            _quotevolume = "NULL"
            _weightedaverage = "NULL"
            _sma_7 = "NULL"
            _ema_7 = "NULL"
            _sma_30 ="NULL"
            _ema_30 = "NULL"
            _sma_200 ="NULL"
            _ema_200 ="NULL"
            command = "INSERT INTO Coinbase_BTC_EUR_3600 VALUES("+str(_id)+","+_date+","+str(_high)+","+str(_low)+","+str(_open)+","+str(_close)+","+str(_volume)+","+str(_quotevolume)+","+str(_weightedaverage)+","+str(_sma_7)+","+str(_ema_7)+","+str(_sma_30)+","+str(_ema_30)+","+str(_sma_200)+","+str(_ema_200)+")"
            connexion.execute(command)
            connexion.commit()

    connexion.close()

def auto_update_candles():
    last_conn_epoch = get_last_date("basededonnees.db")
    last_conn_iso = convertEpochIso8601(last_conn_epoch)
    now_conn_iso = datetime.datetime.now().replace(microsecond=0).isoformat() + "Z"
    now_conn_epoch = ISO_to_Epoch(now_conn_iso)
    nb_days = (now_conn_epoch - last_conn_epoch)/(60*60*24)
    if(nb_days>10):
        j = int(nb_days/10)+1
        more_candles(j,str(last_conn_iso),str(now_conn_iso))
    if(nb_days<0.042):
        more_candles(0,str(last_conn_iso),str(now_conn_iso))
    else:
        more_candles(1,str(last_conn_iso),str(now_conn_iso))

class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = (timestamp + request.method + request.path_url + (request.body or ''))
        message = message.encode('ascii')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


def afficherContenuPortefeuille():
    api_url = 'https://api-public.sandbox.pro.coinbase.com/'
    auth = CoinbaseExchangeAuth(api_key = import_log()['log'], secret_key = import_log()['secret'], passphrase = import_log()['passphrase'])
    r = requests.get(api_url + 'accounts', auth=auth)
    for all in r.json():
        print(str(all['currency']+" : "+str(all['balance'])))

def getAnOrder():
    api_url = 'https://api-public.sandbox.pro.coinbase.com/'
    auth = CoinbaseExchangeAuth(api_key = import_log()['log'], secret_key = import_log()['secret'], passphrase = import_log()['passphrase'])
    r = requests.delete(api_url + 'orders', auth=auth)
    print (r.json())
