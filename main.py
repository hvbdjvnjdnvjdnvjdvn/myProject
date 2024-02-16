import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import Table, Column, Integer, String



DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
users = Table("users", metadata,
              Column("id", Integer, primary_key=True),
              Column("username", String),
              Column("lastname", String),
              Column("email", String),
              Column("password", String))


products = Table("products", metadata,
              Column("id", Integer, primary_key=True),
              Column("userproducts", String),
              Column("description", String),
              Column("price", String))


orders = Table("orders", metadata,
              Column("id", Integer, primary_key=True),
              Column("user_id", Integer, foreign_key=True),
              Column("products_id", Integer, foreign_key=True),
              Column("time", String),
              Column("status", String))
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)



class User(BaseModel):
    username: str
    lastname: str
    email: str
    password: str


class UserID(User):
    id: int


class Product(BaseModel):
    userproducts: str
    userproducts: str
    description: str
    price: str


class ProductID(Product):
    id: int


class Order(BaseModel):
    time: str
    status: str


class OrderID(Order):
    id: int
    user_id: int
    products_id: int



    
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def get_useers():
    return {"Hello": "World"}



@app.get("/users/", response_model=list[UserID])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}")
async def get_users(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)



@app.get("/products/", response_model=list[ProductID])
async def get_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get("/orders/", response_model=list[OrderID])
async def get_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{products_id}")
async def get_orders(products_id: int):
    query = orders.select().where(orders.c.id == products_id)
    return await database.fetch_one(query)



