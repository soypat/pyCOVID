import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

class Country:
    def __init__(self, name):
        self.name = name
        self.totalCases = []
        self.date = []
        self.totalDeaths = []

    def AddCases(self, date, totalCases, totalDeaths):
        self.totalCases.append(totalCases)
        self.totalDeaths.append(totalDeaths)
        self.date.append(date)

    def PlotCases(self):
        ax = self.newAxes()
        ax.set_xlabel('Fecha [Y-m-d]')
        ax.set_ylabel('Casos Confirmados')
        ax.set_title('Casos confirmados en ' + self.name)
        plt.plot(self.date, self.totalCases)
        plt.xticks(rotation=45)

    def PlotCasesLog(self):
        ax = self.newAxes()
        ax.set_xlabel('Fecha [Y-m-d]')
        ax.set_ylabel('Casos Confirmados')
        ax.set_title('Casos confirmados en ' + self.name + ' (log scale)')
        plt.semilogy(self.date, self.totalCases)
        plt.xticks(rotation=45)

    def newAxes(self):
        plt.figure()
        ax = plt.gca()
        formatter = mdates.DateFormatter("%Y-%m-%d")
        ax.xaxis.set_major_formatter(formatter)
        locator = mdates.DayLocator()
        ax.xaxis.set_major_locator(locator)
        return ax

# date,location,new_cases,new_deaths,total_cases,total_deaths
############################
##  INSERT YOUR COUNTRY   ##
############################
myCountryName = 'Argentina'

fullFilename = 'data.csv'
dateFormat = '%Y-%m-%d'
CVD = pd.read_csv(fullFilename)
CVDcountry = {}
Nfull = len(CVD['date'])
for i in range(Nfull):
    if CVD['total_cases'][i] == 0 and CVD['total_deaths'][i] == 0:  # Salteamos fechas sin casos
        continue
    loc = CVD['location'][i]
    date = datetime.datetime.strptime(CVD['date'][i], dateFormat)
    countryPresent = False if CVDcountry.get(loc) == None else True
    if not countryPresent:
        CVDcountry[loc] = Country(loc)
    CVDcountry[loc].AddCases(date, CVD['total_cases'][i], CVD['total_deaths'][i])

CVDcountry[myCountryName].PlotCases()
CVDcountry[myCountryName].PlotCasesLog()
