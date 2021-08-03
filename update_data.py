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


fichier = open("previous_date.txt","r")
old_date = fichier.read()
fichier.close()
old_date=old_date[0:len(old_date)-1]

if (old_date == date):
    sys.exit(0)

fichier = open("previous_date.txt","w")
fichier.write(date)
fichier.close()


URL = "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv"
r = requests.get(URL,allow_redirects=True)
open('data_%s.csv'%date,'wb').write(r.content)


data_old = pd.read_csv('data_%s.csv'%old_date)
data_new = pd.read_csv('data_%s.csv'%date)
df_update = data_new.copy()


connexion = mysql.connector.connect(host="localhost",user="machine",password="123456",database="SARS_COV_2")
curseur = connexion.cursor()

#for i in range(data_new.shape[0]):
#	present = False
#	for j in range(data_old.shape[0]):
#		if data_new["dateRep"].loc[i]==data_old["dateRep"].loc[j]:
#			if data_new["day"].loc[i]==data_old["day"].loc[j]:
#				if data_new["month"].loc[i]==data_old["month"].loc[j]:
#					if data_new["year"].loc[i]==data_old["year"].loc[j]:
#						if data_new["cases"].loc[i]==data_old["cases"].loc[j]:
#							if data_new["deaths"].loc[i]==data_old["deaths"].loc[j]:
#								if data_new["countriesAndTerritories"].loc[i]==data_old["countriesAndTerritories"].loc[j]:
#									if data_new["geoId"].loc[i]==data_old["geoId"].loc[j]:
#										if data_new["countryterritoryCode"].loc[i]==data_old["countryterritoryCode"].loc[j]:
#											if data_new["popData2020"].loc[i]==data_old["popData2020"].loc[j]:
#												if data_new["continentExp"].loc[i]==data_old["continentExp"].loc[j]:
#													present=True
#	if present==True:
#		continue
#	else:
#		request = "insert into data_per_day values (\'%s\',%i,%i,%i,%i,%i,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(data_new["dateRep"].loc[i],data_new["day"].loc[i],data_new["month"].loc[i],data_new["year"].loc[i],data_new["cases"].loc[i],data_new["deaths"].loc[i],data_new["countriesAndTerritories"].loc[i],data_new["geoId"].loc[i],data_new["countryterritoryCode"].loc[i],data_new["popData2020"].loc[i],data_new["continentExp"].loc[i])
#		print(request)
fichier = open('insertion_update.sql',"w")

for i in range(data_new.shape[0]):
    liste=data_old.eq(data_new.loc[i]).all(axis=1)
    liste = liste.tolist()
    if True in liste:
        continue
    else:
        request = "insert into data_per_day values (\'%s\',%s,%s,%s,%s,%s,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(data_new["dateRep"].loc[i],data_new["day"].loc[i],data_new["month"].loc[i],data_new["year"].loc[i],data_new["cases"].loc[i],data_new["deaths"].loc[i],data_new["countriesAndTerritories"].loc[i],data_new["geoId"].loc[i],data_new["countryterritoryCode"].loc[i],data_new["popData2020"].loc[i],data_new["continentExp"].loc[i])
        print(request)
        try:
            fichier.write(request)
            curseur.execute(request)
        except:
            request = 'update data_per_day set dateRep=\'%s\', day=%s, month=%s, year=%s, cases=%s, death=%s, countriesAndTerritories=\'%s\', geoId=\'%s\', countryterritoryCode=\'%s\', popData2020=\'%s\', continentExp=\'%s\' where dateRep=\'%s\' and geoId=\'%s\';'%(data_new["dateRep"].loc[i],data_new["day"].loc[i],data_new["month"].loc[i],data_new["year"].loc[i],data_new["cases"].loc[i],data_new["deaths"].loc[i],data_new["countriesAndTerritories"].loc[i],data_new["geoId"].loc[i],data_new["countryterritoryCode"].loc[i],data_new["popData2020"].loc[i],data_new["continentExp"].loc[i],data_new["dateRep"].loc[i],data_new["geoId"].loc[i])
            fichier.write(request)
            curseur.execute(request)
fichier.close()
connexion.commit()		
connexion.close()
curseur.close()

#request = 'select * from data_per_day where dateRep=\'02/08/2021\';'
#curseur.execute(request)
#resultat = curseur.fetchall()
#for resust in resultat:
#	print(resust)



