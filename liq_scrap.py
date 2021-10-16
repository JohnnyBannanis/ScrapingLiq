import requests
import math
from bs4 import BeautifulSoup


def scraping(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    array = []
    data = {}
    for cat in soup.select( 'div[data-id]'):
        categoryName = cat["data-id"]
        categoryNameUpper  = categoryName.replace("/liq-","").upper()
        data[categoryNameUpper] = {}
        prods = []
        cantidad = int(soup.select_one('div[data-id="'+categoryName+'"] div.product-filters__heading h4.link.color-primary-1 span:nth-child(2)').text)
        if int(cantidad) <= 48:
            for i in cat.find_all('div', class_='product'):  
                a = {}
                a["name"] = i.find('div', class_='price color-dark-2 product__card-title').text.replace("LIQ - ","")
                a["price"] = i.find('div', class_='title-md color-primary-1').text
                a["image"] = "https://www.pcfactory.cl/" + i.find('img')['src']
                a["url"] = "https://www.pcfactory.cl/" + i.find('a')['href']
                prods.append(a)
            data[categoryNameUpper] = prods
        else:
            for i in range(1, math.ceil(cantidad/48)+1):
                newurl = "https://www.pcfactory.cl"+categoryName+"?orden=2&pagina="+str(i)
                soup2 = BeautifulSoup(newurl,"html.parser")
                for i in soup2.find_all('div', class_='product'):  
                    a = {}
                    a["name"] = i.find('div', class_='price color-dark-2 product__card-title').text.replace("LIQ - ","")
                    a["price"] = i.find('div', class_='title-md color-primary-1').text
                    a["image"] = "https://www.pcfactory.cl/" + i.find('img')['src']
                    a["url"] = "https://www.pcfactory.cl/" + i.find('a')['href']
                    prods.append(a)
                data[categoryNameUpper] = prods


    return data


