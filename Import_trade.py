import requests
import json
import time
import datetime
import sqlite3
import threading
#############################################################
#DERNIERE QUESTION

def get_trade(name):
    response = requests.get("https://api.pro.coinbase.com/products/"+name+"/trades").json()
    return response
def ISO_to_Epoch(date):
    ref = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    epoch_time = int((ref - datetime.datetime(1970, 1, 1)).total_seconds())
    return epoch_time
    
connexion = sqlite3.connect("basededonnees.db")
curseur = connexion.cursor()  #Récupération d'un curseur
exchangeName = "Coinbase"
pair =  "BTC_EUR"
setTableName = str(exchangeName + "_" + pair)
tableCreationStatement = tableCreationStatement = """CREATE TABLE """ + setTableName + """(Id INTEGER PRIMARY KEY, uuid TEXT, traded_btc REAL, price REAL, created_at_int INT, side TEXT)"""
curseur.execute(tableCreationStatement)
connexion.commit()
reponse = get_trade("BTC-EUR")
for i in range(0,100):
    _id = 100-i
    _created_at_int = ISO_to_Epoch(str(reponse[i]['time']))
    _uuid = reponse[i]['trade_id']
    _price = reponse[i]['price']
    _traded_btc = reponse[i]['size']
    _side = reponse[i]['side']
    params = (_id,_uuid,_traded_btc,_price,_created_at_int,_side)
    connexion.execute("INSERT INTO "+setTableName+" VALUES (?, ?, ?, ?, ?, ?)", params)
    connexion.commit()
#connexion.execute("DROP TABLE Coinbase_BTC_EUR")
connexion.close()