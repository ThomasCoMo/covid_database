#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import sys
import pandas as pd
import requests
import mysql.connector

now = datetime.now()
date = now.strftime("%d-%m-%Y")

fichier = open("previous_date.txt","w")
fichier.write(date)
fichier.close()


URL = "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv"
r = requests.get(URL,allow_redirects=True)
open('data_%s.csv'%date,'wb').write(r.content)

data_new = pd.read_csv('data_%s.csv'%date)
connexion = mysql.connector.connect(host="localhost",user="machine",password="123456",database="SARS_COV_2")
curseur = connexion.cursor()

for i in range(data_new.shape[0]):
    request = "insert into data_per_day values (\'%s\',%s,%s,%s,%s,%s,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(data_new["dateRep"].loc[i],data_new["day"].loc[i],data_new["month"].loc[i],data_new["year"].loc[i],data_new["cases"].loc[i],data_new["deaths"].loc[i],data_new["countriesAndTerritories"].loc[i],data_new["geoId"].loc[i],data_new["countryterritoryCode"].loc[i],data_new["popData2020"].loc[i],data_new["continentExp"].loc[i])
    curseur.execute(request)

connexion.commit()		
connexion.close()
curseur.close()
