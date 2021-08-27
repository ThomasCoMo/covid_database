#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import sys
import requests
import mysql.connector
import tkinter as tk
from tkinter import *
from datetime import datetime
import matplotlib.pyplot as plt

# connexion to database
connexion = mysql.connector.connect(
    host="localhost", user="machine", password="123456", database="SARS_COV_2")
curseur = connexion.cursor()

# get list of countries
#request = 'select countriesAndTerritories From data_per_day group by countriesAndTerritories;'
request = 'select countriesAndTerritories, popData2020 From data_per_day group by countriesAndTerritories, popData2020;'

curseur.execute(request)
liste_countries_pop = []
dico_pop = {}
for line in curseur:
    liste_countries_pop.append(line[0])
    dico_pop[line[0]]=int(line[1])


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_liste()
        self.pays = ""
        self.create_caseacocher()
        self.create_button()
        self.liste_date = []
        self.liste_cases = []
        self.liste_deaths = []
        self.Check=1
        self.isCanevas = False

    def create_liste(self):
        self.liste = Listbox(self)
        for i in range(len(liste_countries_pop)):
            self.liste.insert(i, liste_countries_pop[i])
        self.liste.grid(row=1,column=1)

    def create_caseacocher(self):
        self.ivCheck = IntVar()
        self.ivCheck.set('1')
        self.check_button = tk.Checkbutton(self,text='normalization',variable=self.ivCheck)
        self.check_button.grid(row=2,column=1)

    def create_button(self):
        self.get_button = tk.Button(self)
        self.get_button["text"] = 'select country and plot'
        self.get_button["command"] = self.Execute
        self.get_button.grid(row=3,column=1)

    def create_canevas(self):
        photo = PhotoImage(file='graph.png')
        self.canvas = Canvas(self,width=640, height=480)
        self.canvas.create_image(0, 0, anchor=NW, image=photo)
        self.canvas.image=photo
        self.canvas.grid(row=4,column=1)
        self.isCanevas=True
        
    def get_values_to_plot(self):
        request = 'select dateRep, cases, death from data_per_day where countriesAndTerritories=\'%s\';' % self.pays
        liste_date = []
        liste_cases = []
        liste_deaths = []
        curseur.execute(request)
        liste_inter=[]
        self.Check=self.ivCheck.get()
        for i in curseur:
            liste_inter.append([datetime.strptime(i[0], '%d/%m/%Y'),i[1],i[2]])
        liste_inter.sort()
        #print(liste_inter)
        if self.Check==1:
            for line in liste_inter:
                #print(line)
                liste_date.append(line[0])
                liste_cases.append(line[1]/dico_pop[self.pays]*100000)
                liste_deaths.append(line[2]/dico_pop[self.pays]*100000)
        if self.Check==0:
            for line in liste_inter:
                #print(line)
                liste_date.append(line[0])
                liste_cases.append(line[1])
                liste_deaths.append(line[2])
        self.liste_date = liste_date
        self.liste_cases = liste_cases
        self.liste_deaths = liste_deaths
        #print(liste_date)
        #dates=matplotlib.dates.date2num(self.liste_date)
        #matplotlib.pyplot.plot_date(dates, self.cases)
        fig = plt.figure()
        plt.plot(self.liste_date[1:],self.liste_cases[1:],'r-',label='cases')
        plt.plot(self.liste_date[1:],self.liste_deaths[1:],'b-',label='deaths')
        if self.Check==1:
            plt.title('number of cases and deaths in %s per 100000 inhabitants'%self.pays)
        if self.Check==0:
            plt.title('number of cases and deaths in %s'%self.pays)
        plt.xlabel('dates')
        plt.ylabel('number of cases/deaths')
        plt.legend()
        plt.gcf().autofmt_xdate()
        fig.savefig('graph.png')

    def get_country(self):
        self.pays=self.liste.get(self.liste.curselection())
        print(self.pays)

    def Execute(self):
        self.get_country()
        self.get_values_to_plot()
        self.create_canevas()

    def create_widgets(self):
        self.hi_there=tk.Button(self)
        self.hi_there["text"]="Hello World\n(click me)"
        self.hi_there["command"]=self.say_hi
        self.hi_there.pack(side="top")

        self.quit=tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")


root=tk.Tk()
app=Application(master=root)
app.mainloop()
