from pydantic import BaseModel
from typing import Optional
import sqlite3

DATABASE= "inventory.db"

def db_connection():
    conn = sqlite3.connect(DATABASE)    
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    conn=db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price INTEGER NOT NULL,
            category TEXT NOT NULL
            )
            ''')
    
    conn.commit()
    conn.close()

class Product(BaseModel):
   
    name:str
    quantity:int
    price:int
    category:str
    
class ProductUpdateRequest(BaseModel):
    name:   Optional[str]=None
    quantity:   Optional[int]=None
    price:   Optional[int]=None
    category: Optional[str]=None