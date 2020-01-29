import csv , os
import requests
import json
import time
#os.system("clear")

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

array = get_all_products()
print(array)