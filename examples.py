############################
##        EXAMPLES        ##
############################
from pycvd import World

loc = 'Argentina'
southamerica = ['Argentina', 'Brazil', 'Uruguay', 'Venezuela', 'Peru', 'Chile', 'Ecuador', 'Colombia', 'Paraguay',
                'Bolivia']
world = World(dir='data', download=True)  # To download dataset, set parameter download to True
world.PlotCompareCasesLog(50, southamerica)

world.Choropleth("01-04-2020", dateFormat="%d-%m-%Y", deaths=False, rollAvg=0) # plots total cases for a given day
for location in world.locCases:
    print(location) # Print all country names

# Other examples of usage
# world.PlotCases('World')
# world.PlotCompareCases(100,['China','United States'])
# world.PlotCases(loc)
# world.PlotCasesLog(loc)
# world.PlotCases('United States')
# world.PlotCasesLog('United States')

