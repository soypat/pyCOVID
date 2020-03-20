# https://covid.ourworldindata.org/data/ecdc/full_data.csv
import requests
# date,location,new_cases,new_deaths,total_cases,total_deaths
fullFilename = 'data.csv'
fullurl = 'https://covid.ourworldindata.org/data/ecdc/full_data.csv'
r = requests.get(fullurl, allow_redirects=True)
with open(fullFilename, 'wb') as f:
    f.write(r.content)
