from itertools import product

from fastapi import FastAPI
from app.routers.buyers_route import router as buyer_router
from app.routers.products_route import router as product_router
from app.routers.orders_route import router as orders_router

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Main page"}


app.include_router(buyer_router)
app.include_router(product_router)
app.include_router(orders_router)
