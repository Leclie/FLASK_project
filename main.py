from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Создаем экземпляр FastAPI
app = FastAPI()

# Создаем экземпляр базы данных
engine = create_engine('sqlite:///shop.db', echo=True)
Base = declarative_base()

# Определяем модели данных
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

    orders = relationship('Order', back_populates='user')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    order_date = Column(String)
    status = Column(String)

    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

    orders = relationship('Order', back_populates='product')

# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Определяем модели данных Pydantic для валидации запросов и ответов
class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

class OrderRequest(BaseModel):
    user_id: int
    product_id: int
    order_date: str
    status: str

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: str
    status: str

class ProductRequest(BaseModel):
    name: str
    description: str
    price: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int

# CRUD операции для пользователей
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserRequest):
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    return new_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserRequest):
    user_db = session.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(user_db, key, value)
    session.commit()
    return user_db

@app.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return user

# CRUD операции для заказов
@app.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderRequest):
    new_order = Order(**order.dict())
    session.add(new_order)
    session.commit()
    return new_order

@app.get("/orders/{order_id}", response_model=OrderResponse)
async def read_order(order_id: int):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order: OrderRequest):
    order_db = session.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.dict().items():
        setattr(order_db, key, value)
    session.commit()
    return order_db

@app.delete("/orders/{order_id}", response_model=OrderResponse)
async def delete_order(order_id: int):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(order)
    session.commit()
    return order

# CRUD операции для продуктов
@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductRequest):
    new_product = Product(**product.dict())
    session.add(new_product)
    session.commit()
    return new_product

@app.get("/products/{product_id}", response_model=ProductResponse)
async def read_product(product_id: int):
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductRequest):
    product_db = session.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(product_db, key, value)
    session.commit()
    return product_db

@app.delete("/products/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: int):
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return product

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
