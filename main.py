from fastapi import FastAPI
from routes.categories import categories
from routes.products import products 

app = FastAPI()


@app.get("/")
def root():
    return {"datails":"PcFactory products on sale | 2° hand products"}

app.include_router(products)
app.include_router(categories)


