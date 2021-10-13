import requests
from bs4 import BeautifulSoup

url = "https://www.pcfactory.cl/liquidacion"

def scraping(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    array = []
    data = {}
    for cat in soup.select( 'div[data-id]'):
        categoryName = (cat["data-id"].replace("/liq-","").upper())
        data[categoryName] = {}
        for i in cat.find_all('div', class_='product'):  
            data[categoryName]["name"] = i.find('div', class_='price color-dark-2 product__card-title').text.replace("LIQ - ","")
            data[categoryName]["price"] = i.find('div', class_='title-md color-primary-1').text
            data[categoryName]["image"] = "https://www.pcfactory.cl/" + i.find('img')['src']
            data[categoryName]["url"] = "https://www.pcfactory.cl/" + i.find('a')['href']
    return data

print(scraping(url))