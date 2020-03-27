import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class World:
    def __init__(self, dateStart, dateEnd):
        numdays = (dateEnd - dateStart).days + 1
        self.date = [dateStart + dt.timedelta(days=x) for x in range(numdays)]
        self.locCases = {}
        self.locDeaths = {}
        self.N = numdays
        self.markersize = 4

    def setupCompare(self,baseCases,locs):
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

        # dates = range(imax-imin)

    def PlotCompareCasesLog(self, baseCases, locs, **args):
        ax = self.newAxes()

        if "leadDays" in args:
            leadDays = args["leadDays"]
        else:
            leadDays = -1
        caseidxs = self.setupCompare(baseCases,locs)
        imin, imax = min(caseidxs), max(caseidxs)
        for i in range(len(locs)):
            cases = self.locCases[locs[i]].copy()
            idx = caseidxs[i]
            del cases[0:idx - imin+1]
            plt.semilogy(range(len(cases)), cases, label=locs[i], marker=6, linestyle='dashed',linewidth=1, markersize=self.markersize)
            ax.legend()
        ax.set_ylabel('Confirmed cases (log)')
        ax.set_xlabel('Days')
        ax.set_title('CVD19 - Superposition of confirmed cases on case #%s' % baseCases)

    def PlotCompareCases(self, baseCases, locs, **args):
        ax = self.newAxes()
        ax.set_ylabel('Casos Confirmados')
        if "leadDays" in args:
            leadDays = args["leadDays"]
        else:
            leadDays = -1
        caseidxs = self.setupCompare(baseCases,locs)
        imin, imax = min(caseidxs), max(caseidxs)
        for i in range(len(locs)):
            cases = self.locCases[locs[i]].copy()
            idx = caseidxs[i]
            del cases[0:idx - imin]
            plt.plot(range(len(cases)), cases, label=locs[i],marker=6, linestyle='dashed',linewidth=1, markersize=self.markersize)
            ax.legend()
        ax.set_ylabel('Confirmed cases')
        ax.set_xlabel('Days')
        ax.set_title('CVD19 - Superposition of confirmed cases on case #%s' % baseCases)

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

    def newAxes(self):
        plt.figure()
        ax = plt.gca()
        return ax


# date,location,new_cases,new_deaths,total_cases,total_deaths
fullFilename = 'data/full_data.csv'
dateFormat = '%Y-%m-%d'

CVD = pd.read_csv(fullFilename)
CVD['date'] = [dt.datetime.strptime(x, dateFormat) for x in CVD['date']]  # Convert string to datetime
dateEnd, dateStart = max(CVD['date']), min(CVD['date'])
world = World(dateStart, dateEnd)
Nfull = len(CVD['date'])
for i in range(Nfull):
    # cases = CVD['total_cases'][i]
    # deaths = CVD['total_deaths'][i]
    ncases = CVD['new_cases'][i]
    ndeaths = CVD['new_deaths'][i]
    loc = CVD['location'][i]
    date = CVD['date'][i]
    globDateIndex = world.date.index(date)
    countryPresent = False if world.locCases.get(loc) == None else True
    if not countryPresent:
        world.locDeaths[loc] = [None if x < globDateIndex else 0 for x in range(world.N)]
        world.locCases[loc] = [None if x < globDateIndex else 0 for x in range(world.N)]
    world.locCases[loc][globDateIndex::] = [x + ncases for x in world.locCases[loc][globDateIndex::]]
    world.locDeaths[loc][globDateIndex::] = [x + ndeaths for x in world.locDeaths[loc][globDateIndex::]]

############################
##        EXAMPLES        ##
############################
plt.close('all')

loc = 'Argentina'
southamerica = ['Argentina','Brazil','Venezuela','Peru','Chile','Ecuador','Colombia','Paraguay','Bolivia']
world.PlotCompareCasesLog(50, southamerica)
world.PlotCompareCases(100,['China','United States'])
plt.show()
world.PlotCases(loc)
world.PlotCasesLog(loc)
plt.show()
world.PlotCases('United States')
world.PlotCasesLog('United States')
world.PlotCases('World')
