import uuid

from fastapi import FastAPI

from product import TProduct

app = FastAPI()

products = {}


@app.get("/list_products")
def list_products():
    return products


@app.get("/get_product")
def get_product(id: str):
    return products.get(id)


@app.post("/add_new_product")
def add_new_product(product: TProduct):
    id = str(uuid.uuid1())
    products[id] = product
    return id, product


@app.put("/change_product")
def change_product(id: str, new_product: TProduct):
    if id in products:
        products[id] = new_product
        return new_product
    return None


@app.delete("/delete_product")
def delete_product(id: str):
    if id in products:
        del products[id]
