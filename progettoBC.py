# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 13:16:41 2022

@author: utente
"""
from datetime import datetime
import requests
import json
import time

class Reporter:
    #metodo costruttore
    def __init__(self):
         self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
         self.params =  {"convert" : "USD"}
         self.headers =  {"Accepts" : "application/json",
           "X-CMC_PRO_API_KEY" : "<your key>"}
         
    #funzione che effettua il report    
    def cryptoReport(self):
        r = requests.get(url = self.url, headers = self.headers, params = self.params).json()
        #dichiarazione e inizializzazione strutture temporanee
        best_volume = dict()           #conterrà la cv col volume maggiore e il nome
        unit_price = dict()           #conterrà il denaro necessario per acquistare una unità delle prime 20 criptovalute e il nome   
        unit_price_vol = dict()           #conterrà il prezzo di una unità delle cv il cui vol nelle 24h > 76mil e il nome
        value_var24h = dict()           #conterrà la variazione di valore nelle ultime 24h con il nome delle prime 20 criptovalute 
        vol_temp = 0            #valore temporaneo del volume per il confronto
        dic_temp = dict()       #diz temporaneo per lo storing delle cv migliori e peggiori 
        best_cryptos = dict()   #conterrà le migliori 10 criptovalute
        worst_cryptos = dict()  #conterrà le peggiori 10 criptovalute 
        cryptos_7days = dict()          #migliore e pegg. cv per la var di valore nell'ultima settimana
        cryptos_30days = dict()         #migliore e pegg. cv per la var di valore nell'ultimo mese
        cryptos_60days = dict()         #migliore e pegg. cv ---     ----       - negli ultimi 60 giorni
        cryptos_90days = dict()         #---       - - ------   -     -   negli ultimi 90 giorni
        
        #inizializzo con valori temporanei che poi andranno confrontati
        best7 = r["data"][0]["quote"]["USD"]["percent_change_7d"]
        worst7 = r["data"][0]["quote"]["USD"]["percent_change_7d"]
        best30 = r["data"][0]["quote"]["USD"]["percent_change_30d"]
        worst30 = r["data"][0]["quote"]["USD"]["percent_change_30d"]
        best60 = r["data"][0]["quote"]["USD"]["percent_change_60d"]
        worst60 = r["data"][0]["quote"]["USD"]["percent_change_60d"]
        best90 = r["data"][0]["quote"]["USD"]["percent_change_90d"]
        worst90 = r["data"][0]["quote"]["USD"]["percent_change_90d"]
        
        #scorro tutte le criptovalute
        for currency in r["data"]:
            #eseguo i confronti con i rispettivi valori temporanei
            if currency["quote"]["USD"]["volume_24h"] > vol_temp:
                vol_temp = currency["quote"]["USD"]["volume_24h"]
                max_vol_curr = currency["name"]
            if currency["quote"]["USD"]["percent_change_7d"] > best7:
                best_change7days = currency["quote"]["USD"]["percent_change_7d"]
                best_crypto7days = currency["name"]
            if currency["quote"]["USD"]["percent_change_7d"] < worst7:
                worst_change7days = currency["quote"]["USD"]["percent_change_7d"]
                worst_crypto7days = currency["name"]
            if currency["quote"]["USD"]["percent_change_30d"] > best30:
                best_change30days = currency["quote"]["USD"]["percent_change_30d"]
                best_crypto30days = currency["name"]
            if currency["quote"]["USD"]["percent_change_30d"] < worst30:
                worst_change30days = currency["quote"]["USD"]["percent_change_30d"]
                worst_crypto30days = currency["name"]
            if currency["quote"]["USD"]["percent_change_60d"] > best60:
                best_change60days = currency["quote"]["USD"]["percent_change_60d"]
                best_crypto60days = currency["name"]
            if currency["quote"]["USD"]["percent_change_60d"] < worst60:
                worst_change60days = currency["quote"]["USD"]["percent_change_60d"]
                worst_crypto60days = currency["name"]
            if currency["quote"]["USD"]["percent_change_90d"] > best90:
                best_change90days = currency["quote"]["USD"]["percent_change_90d"]
                best_crypto90days = currency["name"]
            if currency["quote"]["USD"]["percent_change_90d"] < worst90:
                worst_change90days = currency["quote"]["USD"]["percent_change_90d"]
                worst_crypto90days = currency["name"]
            #inserisco tutte le cv nel diz temporaneo corrispondente   
            dic_temp[currency["name"]] = currency["quote"]["USD"]["percent_change_24h"]
            #inserisco dati nel dizionario con la condizione
            if currency["quote"]["USD"]["volume_24h"] > 76000000:
                unit_price_vol[currency["name"]] = round((currency["quote"]["USD"]["price"]),2)
                
        #aggiorno i diz una volta finito il ciclo
        best_volume[max_vol_curr] = vol_temp
        cryptos_7days[best_crypto7days] = best_change7days
        cryptos_7days[worst_crypto7days] = worst_change7days
        cryptos_30days[best_crypto30days] = best_change30days
        cryptos_30days[worst_crypto30days] = worst_change30days
        cryptos_60days[best_crypto60days] = best_change60days
        cryptos_60days[worst_crypto60days] = worst_change60days
        cryptos_90days[best_crypto90days] = best_change90days
        cryptos_90days[worst_crypto90days] = worst_change90days
        #ordino il diz temporaneo al contrario
        dic_temp = dict(sorted(dic_temp.items(), key=lambda item: item[1]))
        #aggiorno i dizionari best_cryptos e worst_cryptos partendo dal diz temporaneo
        current_index = 0                   #variabile temporanea
        for key in dic_temp.keys():
            if current_index < 11:
                worst_cryptos[key] = dic_temp[key]
                current_index += 1
        current_index = 0
        for key in reversed(dic_temp.keys()):
            if current_index < 11:
                best_cryptos[key] = dic_temp[key]
                current_index += 1
                
        #effettuo un altro ciclo sugli indici delle prime 20 criptovalute
        for index in range(20):
            #aggiorno il diz con il nome e il prezzo di un'unità della relativa cv
            unit_price[r["data"][index]["name"]] = round((r["data"][index]["quote"]["USD"]["price"]),2)
            #aggiorno il diz con la variazione di valore nelle ultime 24h e il nome della cv
            value_var24h[r["data"][index]["name"]] = r["data"][index]["quote"]["USD"]["percent_change_24h"]
        
        #strutturo tutti i dati che ho ottenuto in un dizionario per salvarlo in un file json
        output_dict = dict()
        output_dict["Criptovaluta col volume maggiore nelle ultime 24h"] = best_volume
        output_dict["Le 10 criptovalute migliori"] = best_cryptos
        output_dict["Le 10 criptovalute peggiori"] = worst_cryptos
        output_dict["Quantità di denaro per acquistare un'unità delle prime 20 cv"] = unit_price
        output_dict["Quantità di denaro per acquistare un'unità delle cv con volume > 76mil"] = unit_price_vol
        output_dict["Variazione valore nelle ultime 24h delle prime 20 cv"] = value_var24h
        output_dict["Migliore e pegg. cv per variazione di valore negli ultimi 7 giorni"] = cryptos_7days
        output_dict["Migliore e pegg. cv per variazione di valore negli ultimi 30 giorni"] = cryptos_30days
        output_dict["Migliore e pegg. cv per variazione di valore negli ultimi 60 giorni"] = cryptos_60days
        output_dict["Migliore e pegg. cv per variazione di valore negli ultimi 90 giorni"] = cryptos_90days
        #ritorno il dizionario creato        
        return output_dict
        
#creo un ogg.(bot) di tipo Reporter
reportBot = Reporter()

while(1):
        #faccio eseguire il report al bot
        data = reportBot.cryptoReport()
        #nomino il file di output 
        now = datetime.now()
        name = now.strftime("%d-%m-%Y") + ".json"
        #scrivo sul file di output
        with open(name, "w") as outfile:
            json.dump(data, outfile, indent = 4)
        hours = 24
        minutes = hours * 60
        seconds = minutes * 60
        time.sleep(seconds)
   