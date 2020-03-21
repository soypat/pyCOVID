# https://covid.ourworldindata.org/data/ecdc/full_data.csv
import requests
# date,location,new_cases,new_deaths,total_cases,total_deaths
urls = ['https://covid.ourworldindata.org/data/ecdc/full_data.csv',
        'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson']

for url in urls:
    r = requests.get(url, allow_redirects = True)
    with open('data/'+url[url.rfind('/')+1::], 'wb') as f:
        f.write(r.content)

