from fastapi import FastAPI
from products.prod_route import app as product_router
from orders.order_route import app as order_router
app = FastAPI()
app.include_router(product_router, prefix="/api/v1", tags=["products"])
app.include_router(order_router, prefix="/api/v1", tags=["orders"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
