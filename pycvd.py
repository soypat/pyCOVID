import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import geopandas as gpd
import requests


# date,location,new_cases,new_deaths,total_cases,total_deaths
# https://covid.ourworldindata.org/data/ecdc/full_data.csv

def newAxes():
    plt.figure()
    ax = plt.gca()
    return ax

def getRollAvg(data, span):
    if span==1:
        return data
    N = len(data)
    data = [0 if x is None else x for x in data]
    rollAvg = [None for _ in range(N)]
    forward, backward = (span) // 2, (span - 1) // 2
    for i in range(N):
        tail = data[i-backward:i] if i-backward >= 0 else data[:i]
        head = data[i+1:i+forward+1] if i+forward <= N else data[i+1:]
        rollAvg[i] = (sum(tail) + sum(head) + data[i])/span
    return rollAvg


class World:
    def __init__(self, **args):
        dir = args["dir"] if "dir" in args else 'data'
        download = args["download"] if "download" in args else False
        dateFormat = args["dateFormat"] if "dateFormat" in args else '%Y-%m-%d'
        if download:
            self.downloadData(dir)
        CVD = pd.read_csv(dir + '/' + 'full_data.csv')
        CVD['date'] = [dt.datetime.strptime(x, dateFormat) for x in CVD['date']]  # Convert string to datetime
        dateEnd, dateStart = max(CVD['date']), min(CVD['date'])
        numdays = (dateEnd - dateStart).days + 1
        self.date = [dateStart + dt.timedelta(days=x) for x in range(numdays)]
        self.locCases = {}
        self.locDeaths = {}
        self.locNewCases = {}
        self.locNewDeaths = {}
        self.N = numdays
        self.markersize = 4
        Nfull = len(CVD['date'])
        for i in range(Nfull):
            ncases = CVD['new_cases'][i]
            ndeaths = CVD['new_deaths'][i]
            loc = CVD['location'][i]
            date = CVD['date'][i]
            globDateIndex = self.date.index(date)
            countryPresent = False if self.locCases.get(loc) == None else True
            if not countryPresent:
                self.locNewDeaths[loc] = [None if x < globDateIndex else 0 for x in range(self.N)]
                self.locNewCases[loc] = [None if x < globDateIndex else 0 for x in range(self.N)]
                self.locDeaths[loc] = [None if x < globDateIndex else 0 for x in range(self.N)]
                self.locCases[loc] = [None if x < globDateIndex else 0 for x in range(self.N)]
            self.locNewCases[loc][globDateIndex] = ncases
            self.locNewDeaths[loc][globDateIndex] = ndeaths
            self.locCases[loc][globDateIndex::] = [x + ncases for x in self.locCases[loc][globDateIndex::]]
            self.locDeaths[loc][globDateIndex::] = [x + ndeaths for x in self.locDeaths[loc][globDateIndex::]]
        self.initGeo(dir)

    def downloadData(self, dir):
        urls = ['https://covid.ourworldindata.org/data/ecdc/full_data.csv',
                'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson']
        for url in urls:
            r = requests.get(url, allow_redirects=True)
            with open(dir + '/' + url[url.rfind('/') + 1::], 'wb') as f:
                f.write(r.content)

    def initGeo(self, dir):
        geojsonFilename = dir + '/countries.geojson'
        exclude = ["Antarctica"]
        nameChange = {
            "United States of America": "United States",
            "The Bahamas": "Bahamas",
            "Republic of Congo": "Congo",
            "Democratic Republic of the Congo": "Democratic Republic of Congo",
            "Curaçao": "Curacao"
        }
        excludeIndex = []
        df = gpd.read_file(geojsonFilename)
        for i in range(len(df["ADMIN"])):
            country = df["ADMIN"][i]
            if country in exclude:
                excludeIndex.append(i)
            if country in nameChange:
                df = df.replace(to_replace=country, value=nameChange[country])
        self.geo = df.drop(excludeIndex)

    def setupCompare(self, baseCases, locs):
        caseidxs = []
        for loc in locs:
            appended = False
            for i in range(len(self.locCases[loc])):
                if self.locCases[loc][i] is not None:
                    if self.locCases[loc][i] > baseCases:
                        caseidxs.append(i)
                        appended = True
                        break
            if not appended:
                caseidxs.append(len(self.locCases[loc]))
        return caseidxs

    def PlotCompareCasesLog(self, baseCases, locs, **args):
        ax = newAxes()

        if "leadDays" in args:
            leadDays = args["leadDays"]
        else:
            leadDays = -1
        caseidxs = self.setupCompare(baseCases, locs)
        imin, imax = min(caseidxs), max(caseidxs)
        for i in range(len(locs)):
            cases = self.locCases[locs[i]].copy()
            idx = caseidxs[i]
            del cases[0:idx - imin + 1]
            plt.semilogy(range(len(cases)), cases, label=locs[i], marker=6, linestyle='dashed', linewidth=1,
                         markersize=self.markersize)
            ax.legend()
        ax.set_ylabel('Confirmed cases (log)')
        ax.set_xlabel('Days')
        ax.set_title('CVD19 - Superposition of confirmed cases on case #%s' % baseCases)
        plt.show()

    def PlotCompareCases(self, baseCases, locs, **args):
        ax = newAxes()
        ax.set_ylabel('Casos Confirmados')
        if "leadDays" in args:
            leadDays = args["leadDays"]
        else:
            leadDays = -1
        caseidxs = self.setupCompare(baseCases, locs)
        imin, imax = min(caseidxs), max(caseidxs)
        for i in range(len(locs)):
            cases = self.locCases[locs[i]].copy()
            idx = caseidxs[i]
            del cases[0:idx - imin]
            plt.plot(range(len(cases)), cases, label=locs[i], marker=6, linestyle='dashed', linewidth=1,
                     markersize=self.markersize)
            ax.legend()
        ax.set_ylabel('Confirmed cases')
        ax.set_xlabel('Days')
        ax.set_title('CVD19 - Superposition of confirmed cases on case #%s' % baseCases)
        plt.show()

    def PlotCases(self, loc):
        ax = self.newDateAxes()
        ax.set_ylabel('Confirmed cases')
        ax.set_title('CVD19 - Confirmed cases in ' + loc)
        plt.plot(self.date, self.locCases[loc])
        plt.xticks(rotation=45)
        plt.show()
        return plt.gcf()

    def PlotCasesLog(self, loc):
        ax = self.newDateAxes()
        ax.set_ylabel('Confirmed cases')
        ax.set_title('CVD19 - Confirmed cases in ' + loc + ' (log scale)')
        plt.semilogy(self.date, self.locCases[loc])
        plt.xticks(rotation=45)
        plt.show()
        return plt.gcf()

    def newDateAxes(self):
        plt.figure()
        ax = plt.gca()
        formatter = mdates.DateFormatter("%m-%d")
        ax.xaxis.set_major_formatter(formatter)
        ax.set_xlabel('Fecha [m-d]')
        return ax

    def Choropleth(self, date, **args):
        rollAvg = args["rollAvg"] if "rollAvg" in args else 0  # Graphs total, not new by default
        deaths = args["deaths"] if "deaths" in args else False  # Graphs cases by default
        if deaths:
            data = self.locNewDeaths if rollAvg > 0 else self.locDeaths
        else:
            data = self.locNewCases if rollAvg > 0 else self.locCases
        dateFormat = args["dateFormat"] if "dateFormat" in args else None  # Graphs total, not new by default
        if dateFormat is not None:
            datestr = date
            date = dt.datetime.strptime(datestr, dateFormat)
            dateIndex = self.date.index(date)
        else:
            datestr = date.strftime("%d-%m-%y")
            dateIndex = self.date.index(date)
        geoloc = [x for x in self.geo.ADMIN]
        columnName = "cases"
        geocases = [0 for i in range(len(self.geo.ADMIN))]
        for loc in data:
            if rollAvg>0:
                datum = getRollAvg(data[loc], rollAvg)[dateIndex]
            else:
                datum = data[loc][dateIndex]
            if loc in geoloc:
                geoIndex = geoloc.index(loc)
                geocases[geoIndex] = datum if (datum is not None) else 0
        graphable = self.geo.copy()
        graphable.insert(loc=0, column=columnName, value=geocases)
        ax = graphable.plot(column=columnName)  # column=cases
        #Title Generation
        prefix = "%d day rolling average of new" % (rollAvg) if rollAvg > 0 else "Total"
        if rollAvg==1:
            prefix = "New"
        matter = "deaths" if deaths else "cases"
        ax.set_title('CVD19 - %s %s on day %s' % (prefix,matter,datestr))
        plt.show()
