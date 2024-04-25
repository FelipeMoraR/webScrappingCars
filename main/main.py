import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import io

# Force UTF-8 encoding for the console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://www.chileautos.cl/vehiculos/autos-vehículo/usado-tipo/nissan/sentra/'

def getData(url):
    # This headers helps to make a mimic request, i retrive this on the inspect mode, in the network, i selected one header with the same url. I will add an image to make more easier to understand
    # https://www.youtube.com/watch?v=6RfyXcf_vQo this video helps me a lot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
    }

    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements with the specified attribute value
    #soupCarNames = soup.find_all(attrs={'data-webm-clickvalue': 'sv-title'})
    #carNames = [element.get_text() for element in soupCarNames] #Variable cleaning
    
    return soup

def getNextPage(soup):
    page = soup.find('ul', {'class': 'pagination'})

    if not page.find('a', {'class': 'next disabled'}):
        href = page.find('a', {'class': 'next'}).get('href')
        urlNew = 'https://www.chileautos.cl' + href
        return urlNew
    else:
        return None

while True:
    soup = getData(url)
    url = getNextPage(soup)
    if not url:
        break
    

