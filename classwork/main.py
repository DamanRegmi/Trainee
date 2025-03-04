from fastapi import FastAPI,HTTPException

from models import Product, ProductUpdateRequest, db_connection,init_db

app=FastAPI()

init_db()
ALLOWED_CATEGORIES = {"laptop", "mobile"}

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
    return [dict(product) for product in products ] # List Comprehension

@app.post("/products")
async def new_product(product:Product):
    if product.category not in ALLOWED_CATEGORIES:
        raise HTTPException(
            status_code=422,
            detail=f"Category '{product.category}' is not allowed. Must be one of {ALLOWED_CATEGORIES}"
        )
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
    return {"id": product_id}




# @app.delete("/products/{product_id}")
# async def delete_product(product_id:int):
#     conn = db_connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM products WHERE id=?",(product_id,))
#     if cursor.rowcount==0:
#         conn.close()
#         raise HTTPException(
#         status_code=404,
#         detail=f"Product with id:{product_id} does not exists")
#     conn.commit()
#     conn.close()
#     return{"message":"Deleted Successfully"}   
    
# @app.put("/products/{product_id}")
# async def update_product(product_id:int,product_update: ProductUpdateRequest):
#         conn = db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM products WHERE id=?",(product_id,))
#         product = cursor.fetchone()
       
#         if product is None: 
#             conn.close()   
#             raise HTTPException(
#             status_code=404,
#             detail=f"Product with id:{product_id} does not exists") 
            
                
#         updated_product={
                    
#                     "name":product_update.name if product_update.name is not None else product["name"],
#                     "quantity":product_update.quantity if product_update.quantity is not None else product["quantity"],
#                     "price":product_update.price if product_update.price is not None else product["price"],
#                     "category":product_update.category if product_update.category is not None else product["category"]
#         }
        
#         cursor.execute('''UPDATE products
#                     SET name=?,quantity=?,price=?,category=?
#                     WHERE id = ?''',(updated_product["name"],updated_product["quantity"],updated_product["price"],updated_product["category"],product_id))
        
#         conn.commit()
#         conn.close()
#         return updated_product
        
                  
                 
