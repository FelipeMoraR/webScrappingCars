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

car_data = {
    'Car Name': [],
    'Prices': [],
    'Mileage': [],
}


def getData(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Obtener datos de coches
    carNames = [element.get_text().strip() for element in soup.find_all(attrs={'data-webm-clickvalue': 'sv-title'})]
    carPrices = [price.get_text().strip() for price in soup.find_all(attrs={'data-webm-clickvalue': 'sv-price'})]
    carMileage = [mileage.get_text().strip() for mileage in soup.find_all(attrs={'data-type': 'Odometer'})]

    return carNames, carPrices, carMileage, soup


def equalize_lengths(*args):
    # Obtener la longitud máxima
    max_len = max(map(len, args))
    
    # Rellenar listas más cortas con "N/A"
    for lst in args:
        while len(lst) < max_len:
            lst.append("N/A")


def getNextPage(soup):
    page = soup.find('ul', {'class': 'pagination'})
    
    if page and not page.find('a', {'class': 'page-link next disabled'}):
        href = page.find('a', {'class': 'next'}).get('href')
        return 'https://www.chileautos.cl' + href
    else:
        return None

while True:
    carNames, carPrices, carMileage, soup = getData(url)

   
    equalize_lengths(carNames, carPrices, carMileage)

    # Agregar datos a car_data
    car_data['Car Name'].extend(carNames)
    car_data['Prices'].extend(carPrices)
    car_data['Mileage'].extend(carMileage)

    url = getNextPage(soup)
    if not url:
        break


df = pd.DataFrame(car_data)


file_name = 'car_data.xlsx'
df.to_excel(file_name, index=False)

print(f"Excel file created: {file_name}")
