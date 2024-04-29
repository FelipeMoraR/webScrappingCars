import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import io

# Force UTF-8 encoding for the console
# This headers helps to make a mimic request, i retrive this on the inspect mode, in the network, i selected one header with the same url. I will add an image to make more easier to understand
# https://www.youtube.com/watch?v=6RfyXcf_vQo this video helps me a lot
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://www.chileautos.cl/vehiculos/autos-vehículo/usado-tipo/nissan/sentra/'

arrayCars = []

car_data = {
    'Car Name': [],
    'Prices': [],
    'Mileage': [],
    'FuelEconomy': []
}

def cleanData(data):
    if data:
        cleanData = data.get_text().strip()
    else:
        cleanData = 'Null'
    
    return cleanData

def getData(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    #carCard = soup.find_all(attrs={'class':'listing-item card showcase'})
    carCard = soup.select(".listing-item.card.showcase, .listing-item.card.standard")

    for car in carCard:
        dataCarContainer = car.find(attrs = {'class':'card-body'})


        titleElement = dataCarContainer.find(attrs = {'data-webm-clickvalue': 'sv-title'})
        titleCar = cleanData(titleElement)


        priceElement = dataCarContainer.find(attrs={'data-webm-clickvalue': 'sv-price'})
        priceCar = cleanData(priceElement)


        mileageElement = dataCarContainer.find(attrs={'data-type': 'Odometer'})
        mileageCar = cleanData(mileageElement)


        fuelEconomyElement = dataCarContainer.find(attrs = {'data-type': 'Fuel Economy'})
        fuelEconomyCar = cleanData(fuelEconomyElement)

        arrayCars.append([titleCar, priceCar, mileageCar, fuelEconomyCar])

    return soup

def getNextPage(soup):
    page = soup.find('ul', {'class': 'pagination'})
    
    if page and not page.find('a', {'class': 'page-link next disabled'}):
        href = page.find('a', {'class': 'next'}).get('href')
        return 'https://www.chileautos.cl' + href
    else:
        return None

while True:
    soup = getData(url)
    url = getNextPage(soup)
    if not url:
        break

for car in arrayCars:
    car_data['Car Name'].append(car[0])
    car_data['Prices'].append(car[1])
    car_data['Mileage'].append(car[2])
    car_data['FuelEconomy'].append(car[3])


df = pd.DataFrame(car_data)


file_name = 'car_data.xlsx'
df.to_excel(file_name, index=False)

print(f"Excel file created: {file_name}")
