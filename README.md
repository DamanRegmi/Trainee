# Project Overview  

This repository contains multiple tasks involving FastAPI, SQLite, and data processing. It includes an inventory management system, web scraping, data refinement, and CSV integration.  

---

## Task 1 (Feb 4)  

### Description  
- Used FastAPI for an inventory management system.  
- Used SQLite database for data storage.  

### File Name 
- **models.py**  
  - Database initialization and connection.  
  - Product and product update class.  
- **main.py**  
  - FastAPI implementation.  
  - CRUD operations for products.  

### Code to Run  
```bash
uvicorn main:app --reload
```
---

 # Task 2(Feb 11)
 
 - Scrapped lapotp details from single page.
 - Scrapped mobile details from multiple pages.
 ### File Name
 - **scrap.ipynb**
---

 # Task 3(Feb 14)
 
### Task A
- Refined the task 2 code.
- Obtained clean dataset.
- CSV conversion.
### File Name 
- **scrapping.ipynb**
### Task B
- Loaded csv file using fastapi
- Stored in sqlite database
###  File name
- **all.ipynb**
### Code to run 
``` bash 
uvicorn all:app --reload
```
---



