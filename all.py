from fastapi import FastAPI,HTTPException
import pandas as pd
import sqlite3
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
DB="fastapi.db"
csv_file="scrapped_products.csv"

def load_csv_to_db():
    df=pd.read_csv(csv_file)
    
    conn=sqlite3.connect(DB)
    cursor=conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS products(Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Tag TEXT,Name TEXT,Oldprice INTEGER,Newprice INTEGER,
                    Category TEXT,Imgurl TEXT)''')
    df.to_sql('products',conn,if_exists='append',index=False)
    conn.commit()
    conn.close()
    return {
        "Message":"CSV data loaded into database"
    }
    
@app.post("/loadcsv")
def  insert_csv():
    return load_csv_to_db()

@app.get("/products/all")
def get_all_products():
    conn=sqlite3.connect(DB)
    df=pd.read_sql_query("SELECT * FROM products",conn)
    conn.close()
    return df.to_dict(orient="records") 

@app.get("/products")
def get_product(id:int):
    conn=sqlite3.connect(DB)
    
    df=pd.read_sql_query("SELECT * FROM products WHERE Id=? ",conn,params=[id])
    conn.close()
    return df.to_dict(orient="records") 


class Product(BaseModel):
    Tag: str
    Name:str
    Oldprice:int
    Newprice:int
    Category:str
    Imgurl:str
    
class ProductUpdateRequest(BaseModel):
    Tag:Optional[str]=None
    Name:Optional[str]=None
    Oldprice:Optional[int]=None
    Newprice:Optional[int]=None
    Category:Optional[str]=None
    Imgurl:Optional[str]=None   
    
    

@app.post("/product")
def post_product(product:Product):
    conn=sqlite3.connect(DB)
    cursor=conn.cursor()
    cursor.execute('''INSERT INTO products (Tag,Name,Oldprice,Newprice,Category,Imgurl)
                         VALUES (?,?,?,?,?,?)''',(product.Tag,product.Name,product.Oldprice,product.Newprice,product.Category,product.Imgurl))
    conn.commit()
    conn.close()
    return{
        "Message":"Inserted successfully!"
    }
    
@app.put("/product")
def update_product(id:int,product_update: ProductUpdateRequest):
    conn=sqlite3.connect(DB)
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id=?",(id,))
    product=cursor.fetchone()
    if product is None: 
            conn.close()   
            raise HTTPException(
            status_code=404,
            detail=f"Product with id:{id} does not exists") 
            
                
    updated_product={
            "Tag":product_update.Tag if product_update.Tag is not None else product["Tag"],       
            "Name":product_update.Name if product_update.Name is not None else product["Name"],
            "Oldprice":product_update.Oldprice if product_update.Oldprice is not None else product["Oldprice"],
            "Newprice":product_update.Newprice if product_update.Newprice is not None else product["Newprice"],
            "Category":product_update.Category if product_update.Category is not None else product["Category"],
            "Imgurl":product_update.Imgurl if product_update.Imgurl is not None else product["Imgurl"]
            
        }
        
    cursor.execute('''UPDATE products
                    SET Tag=?,Name=?,Oldprice=?,Newprice=?,Category=?,Imgurl=?
                    WHERE id = ?''',(updated_product["Tag"],updated_product["Name"],updated_product["Oldprice"],updated_product["Newprice"],updated_product["Category"],updated_product["Imgurl"],id))
        
    conn.commit()
    conn.close()
    return updated_product

@app.delete("/products/{id}")
async def delete_product(id:int):
    conn =sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?",(id,))
    if cursor.rowcount==0:
        conn.close()
        raise HTTPException(
        status_code=404,
        detail=f"Product with id:{id} does not exists")
    conn.commit()
    conn.close()
    return{"message":"Deleted Successfully"}
  
    
         