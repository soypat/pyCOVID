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

    def PlotCases(self,loc):
        ax = self.newAxes()
        ax.set_ylabel('Casos Confirmados')
        ax.set_title('Casos confirmados en ' + loc)
        plt.plot(self.date, self.locCases[loc])
        plt.xticks(rotation=45)
        return plt.gcf()

    def PlotCasesLog(self, loc):
        ax = self.newAxes()
        ax.set_ylabel('Casos Confirmados')
        ax.set_title('Casos confirmados en ' + loc + ' (log scale)')
        plt.semilogy(self.date, self.locCases[loc])
        plt.xticks(rotation=45)
        return plt.gcf()

    def newAxes(self):
        plt.figure()
        ax = plt.gca()
        formatter = mdates.DateFormatter("%m-%d")
        ax.xaxis.set_major_formatter(formatter)
        ax.set_xlabel('Fecha [m-d]')
        return ax

# date,location,new_cases,new_deaths,total_cases,total_deaths
fullFilename = 'data/full_data.csv'
dateFormat = '%Y-%m-%d'

CVD = pd.read_csv(fullFilename)
CVD['date'] = [dt.datetime.strptime(x,dateFormat) for x in CVD['date']] # Convert string to datetime
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
world.PlotCases(loc)
world.PlotCasesLog(loc)
world.PlotCases('United States')
world.PlotCases('World')