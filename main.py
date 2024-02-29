from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Модели Pydantic для каждой таблицы
class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str

class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: str
    status: str

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

users_db = []
orders_db = []
products_db = []

# CRUD операции для пользователей
@app.post("/users/", response_model=User)
async def create_user(user: User):
    users_db.append(user)
    return user

@app.get("/users/", response_model=List[User])
async def read_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    for i, u in enumerate(users_db):
        if u.id == user_id:
            users_db[i] = user
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            del users_db[i]
            return user
    raise HTTPException(status_code=404, detail="User not found")

# CRUD операции для заказов
@app.post("/orders/", response_model=Order)
async def create_order(order: Order):
    orders_db.append(order)
    return order

@app.get("/orders/", response_model=List[Order])
async def read_orders():
    return orders_db

@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    for order in orders_db:
        if order.id == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: Order):
    for i, o in enumerate(orders_db):
        if o.id == order_id:
            orders_db[i] = order
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/{order_id}", response_model=Order)
async def delete_order(order_id: int):
    for i, order in enumerate(orders_db):
        if order.id == order_id:
            del orders_db[i]
            return order
    raise HTTPException(status_code=404, detail="Order not found")

# CRUD операции для товаров
@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    products_db.append(product)
    return product

@app.get("/products/", response_model=List[Product])
async def read_products():
    return products_db

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    for product in products_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product):
    for i, p in enumerate(products_db):
        if p.id == product_id:
            products_db[i] = product
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}", response_model=Product)
async def delete_product(product_id: int):
    for i, product in enumerate(products_db):
        if product.id == product_id:
            del products_db[i]
            return product
    raise HTTPException(status_code=404, detail="Product not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
