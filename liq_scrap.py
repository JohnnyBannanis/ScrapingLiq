import requests
import json
import math
from bs4 import BeautifulSoup


url = "https://www.pcfactory.cl/liquidacion?orden=2"

def chunks(l, n):
        n = max(1, n)
        return (l[i:i+n] for i in range(0, len(l), n))

def scraping(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    prod_categories = {}
    prods = []

    #categories listed in the page navigation
    for nav_category in soup.find_all('a', class_ ='landing-liq-btn link link--l color-white'):
        prod_categories[nav_category['href']] = nav_category.text.replace("/","-")

    for category in soup.select( 'div[data-id]'):
        category_href = category["data-id"]
        category_name = prod_categories[category_href]
 
        #pagination, the site only dysplay 48 items max
        cantidad = int(soup.select_one('div[data-id="'+ category_href +'"] div.product-filters__heading h4.link.color-primary-1 span:nth-child(2)').text)
        if int(cantidad) <= 48:
            for i in category.find_all('div', class_='product'):  
                a = {}
                a["id"] = i.find('button', class_='product-ab-link')["data-clipboard-text"]
                a["name"] = i.find('div', class_='price color-dark-2 product__card-title').text.replace("LIQ - ","")
                a["price"] = i.find('div', class_='title-md color-primary-1').text
                a["image"] = i.find('img')['src']
                a["url"] = "https://www.pcfactory.cl/" + i.find('a')['href']
                a["category"] = category_name
                prods.append(a)
        else:
            for i in range(1, math.ceil(cantidad/48)+1):
                newurl = "https://www.pcfactory.cl"+category_href+"?orden=2&pagina="+str(i)
                soup2 = BeautifulSoup(newurl,"html.parser")
                for i in soup2.find_all('div', class_='product'):  
                    a = {}
                    a["id"] = i.find('button', class_='product-ab-link')["data-clipboard-text"]
                    a["name"] = i.find('div', class_='price color-dark-2 product__card-title').text.replace("LIQ - ","")
                    a["price"] = i.find('div', class_='title-md color-primary-1').text
                    a["image"] = i.find('img')['src']
                    a["url"] = "https://www.pcfactory.cl/" + i.find('a')['href']
                    a["category"] = category_name
                    prods.append(a)

    return {"liq" : prods}

def diff():
    with open('db.json') as json_file:
        db = json.load(json_file)
    response = scraping(url)

    in_page = response['liq']
    in_db = db['liq']

    new_items = []
    removed_items = []

    for item in in_page:
        if item not in in_db:
            new_items.append(item)
    for item in in_db:
        if item not in in_page:
            removed_items.append(item)

    if new_items != [] or removed_items != []:
        with open('db.json', 'w') as outfile:
            json.dump(response, outfile)
    return new_items

def read_db():
    with open('db.json') as json_file:
        db = json.load(json_file)
    return db