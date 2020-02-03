from main_functions import obtain_data_candle , obtain_one_candle, verifier_integriter_bd, ISO_to_Epoch, convertEpochIso8601
import sqlite3
import requests
import time

def import_candles():
    connexion = sqlite3.connect("basededonnees.db")
    curseur = connexion.cursor()  #Récupération d'un curseur

    first_date_computable = 1451606400

    exchangeName = "Coinbase"
    pair =  "BTC_EUR"
    duration = str(3600)
    setTableName = str(exchangeName + "_" + pair + "_" + duration)
    #Création de table
    tableCreationStatement = """CREATE TABLE """ + setTableName + """(Id INTEGER PRIMARY KEY, date INT, high REAL, low REAL, open REAL, close REAL, volume REAL, quotevolume REAL, weightedaverage REAL, sma_7 REAL, ema_7 REAL, sma_30 REAL, ema_30 REAL, sma_200 REAL, ema_200 REAL)"""
    curseur.execute(tableCreationStatement)
    connexion.commit()
    list_error =[]
    nb_error = 0


    for i in range(0,149): #0,149
        time = first_date_computable + i * 10*24*3600 #10 jours
        data = obtain_data_candle(name = "BTC-EUR",time = time,duration= 3600)
        for j in range(237): #max == 237 
            try : 
                _id = i*237 + 237-j-1
                _date = str(data[j][0])
                _high = data[j][2]
                _low = data[j][1]
                _open = data[j][3]
                _close = data[j][4]
                _volume = data[j][5]
                _quotevolume = "NULL"
                _weightedaverage = "NULL"
                _sma_7 = "NULL"
                _ema_7 = "NULL"
                _sma_30 ="NULL"
                _ema_30 = "NULL"
                _sma_200 ="NULL"
                _ema_200 ="NULL"

                command = "INSERT INTO "+setTableName+" VALUES("+str(_id)+","+_date+","+str(_high)+","+str(_low)+","+str(_open)+","+str(_close)+","+str(_volume)+","+str(_quotevolume)+","+str(_weightedaverage)+","+str(_sma_7)+","+str(_ema_7)+","+str(_sma_30)+","+str(_ema_30)+","+str(_sma_200)+","+str(_ema_200)+")"
                connexion.execute(command)
                connexion.commit()
            except:
                print("@ERROR")
                nb_error = nb_error+1
                list_error.append(_id)
            print(str(_id/(149*237))+"%       "+"id="+str(_id)+"  i="+str(i)+"  j="+str(j))

    print("#########################################################################")
    print("Il y a eu "+str(nb_error)+ " erreurs soit "+ str(nb_error/(149*237))+"%")
    wait = input("Press enter to go to the next step...")

    taille_prec = 99999999999999
    while len(list_error)<taille_prec:
        taille_prec = len(list_error)
        i =0
        for element in list_error:
            i = i+1
            try :
                time = 3600*element + 1451617200
                _id = element
                data = obtain_one_candle(name = "BTC-EUR",time = time, duration =3600)
                _date = str(data[0])
                _high = data[2]
                _low = data[1]
                _open = data[3]
                _close = data[4]
                _volume = data[5]
                _quotevolume = "NULL"
                _weightedaverage = "NULL"
                _sma_7 = "NULL"
                _ema_7 = "NULL"
                _sma_30 ="NULL"
                _ema_30 = "NULL"
                _sma_200 ="NULL"
                _ema_200 ="NULL"
                command = "INSERT INTO "+setTableName+" VALUES("+str(_id)+","+_date+","+str(_high)+","+str(_low)+","+str(_open)+","+str(_close)+","+str(_volume)+","+str(_quotevolume)+","+str(_weightedaverage)+","+str(_sma_7)+","+str(_ema_7)+","+str(_sma_30)+","+str(_ema_30)+","+str(_sma_200)+","+str(_ema_200)+")"
                connexion.execute(command)
                connexion.commit()
                list_error.remove(element)
                print(str(i/taille_prec)+"%"+" Element ajouté !")
            except:
                print(str(i/taille_prec)+"%"+"ERROR")
        print("Il n'y a plus que : "+str(len(list_error))+" erreurs soit :"+str(len(list_error)/(149*237)) +"%")
        wait = input("Press enter to go to the next step...")

    connexion.close()
def combler_les_trous_Coinbase_BTC_EUR_3600(liste_trou):
    connexion = sqlite3.connect("basededonnees.db")
    i = 0
    j = 0
    while len(liste_trou)>0:
        for element in liste_trou:
            try :
                _time = 3600*element + 1451617200
                _id = element
                data = obtain_one_candle(name = "BTC-EUR",time = _time, duration =3600)
                _date = str(data[0])
                _high = data[2]
                _low = data[1]
                _open = data[3]
                _close = data[4]
                _volume = data[5]
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
                liste_trou.remove(element)
                print("Reussite : "+str(i)+" Echecs : "+str(j))
                i = i+1
            except:
                print("Reussite : "+str(i)+" Echecs : "+str(j))
                j = j+1
            time.sleep(1)
        connexion.close()
    wait = input("Tous est comblé !")

