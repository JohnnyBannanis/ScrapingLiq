from fastapi import APIRouter
from liq_scrap import chunks, scraping, diff

products = APIRouter()
url = "https://www.pcfactory.cl/liquidacion?orden=2"

@products.get("/api/v1/products")
async def fetch_products():
    response = {}
    try:
        response = scraping(url)
    except Exception as ex:
        print(ex)
    return response

@products.get("/api/v1/new")
def new_products():
    response = {}
    try:
        response["data"] = diff()
    except Exception as ex:
        print(ex)
    return response

@products.get("/api/v1/new_group/")
def new_products_group(chunk_size : int = 10):
    response = {}
    try:
        response["data"] = list(chunks(diff(), chunk_size))
    except Exception as ex:
        print(ex)
    return response