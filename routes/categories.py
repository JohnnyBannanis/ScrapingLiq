from fastapi import APIRouter
from liq_scrap import chunks, read_db, scraping

categories = APIRouter()
url = "https://www.pcfactory.cl/liquidacion?orden=2"

#//////////////
#   retrieves data from Live scrapping 
#//////////////
@categories.get("/api/live/categories")
def fetch_categories():
    response = {}
    try:
        catego_list = []
        products = scraping(url)['liq']
        for product in products:
            catego_list.append(product['category'])
        response["data"] = list(set(catego_list))
    except Exception as ex:
        print(ex)
    return response

@categories.get("/api/live/categories/{category}")
def category_products(category: str):
    response = {}
    try:
        products = scraping(url)['liq']
        selected = []
        for product in products:
            if product['category'] == category:
                selected.append(product)
        response["data"] = selected
    except Exception as ex:
        print(ex)
    return response

@categories.get("/api/live/categories_group/{category}/")
def category_products_group(category: str, chunk_size : int = 10):
    response = {}
    try:
        products = scraping(url)['liq']
        selected = []
        for product in products:
            if product['category'] == category:
                selected.append(product)
        response["data"] = list(chunks(selected, chunk_size))
    except Exception as ex:
        print(ex)
    return response

#//////////////
#   retrieves data from DB 
#//////////////
@categories.get("/api/db/categories")
def fetch_categories_db():
    response = {}
    try:
        catego_list = []
        products = read_db()['liq']
        for product in products:
            catego_list.append(product['category'])
        response["data"] = list(set(catego_list))
    except Exception as ex:
        print(ex)
    return response

@categories.get("/api/db/categories/{category}")
def category_products_db(category: str):
    response = {}
    try:
        products = read_db()['liq']
        selected = []
        for product in products:
            if product['category'] == category:
                selected.append(product)
        response["data"] = selected
    except Exception as ex:
        print(ex)
    return response

@categories.get("/api/db/categories_group/{category}/")
def category_products_group_db(category: str, chunk_size : int = 10):
    response = {}
    try:
        products = read_db()['liq']
        selected = []
        for product in products:
            if product['category'] == category:
                selected.append(product)
        response["data"] = list(chunks(selected, chunk_size))
    except Exception as ex:
        print(ex)
    return response