from fastapi import FastAPI,HTTPException
from typing import List
from models import Product, ProductUpdateRequest, db_connection,init_db

app=FastAPI()

init_db()

@app.get("/")
def root():
    return{"Welcome":"This is Inventory Management System"}

@app.get("/products")
async def get_products():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return [dict(product) for product in products ]

@app.post("/products")
async def new_product(product:Product):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products(name,quantity,price,category)
        VALUES(?,?,?,?)
        ''',(product.name,product.quantity,product.price,product.category)
    )
    conn.commit()
    product_id=cursor.lastrowid
    conn.close()
    return {"id":product.id}


@app.delete("/products/{product_id}")
async def delete_product(product_id:int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?",(product_id,))
    if cursor.rowcount==0:
        conn.close()
        raise HTTPException(
        status_code=404,
        detail=f"Product with id:{product_id} does not exists")
    conn.commit()
    conn.close()
    return{"message":"Deleted Successfully"}   
    
@app.put("/products/{product_id}")
async def update_product(product_id:int,product_update: ProductUpdateRequest):
        for i,product in enumerate(db):
            if product.id==product_id:
                updated_product=Product(
                    id=product.id,
                    name=product_update.name if product_update.name is not None else product.name,
                    quantity=product_update.quantity if product_update.quantity is not None else product.quantity,
                    price=product_update.price if product_update.price is not None else product.price,
                    category=product_update.category if product_update.category is not None else product.category
                )
                db[i]=updated_product
                return updated_product
        raise HTTPException(
        status_code=404,
        detail=f"Product with id:{product_id} does not exists"
    )   
                  
                 