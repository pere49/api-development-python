Comprehesive Api development with python course on https://www.youtube.com/watch?v=0sOvCWFmrtA 🔥 :fire:

#### Path Operation for a route
Method -> @app.get
path - > "/"
function -> async def root()

### Api Methods
+ GET
+ POST
+ DELETE
+ PUT

### Working with SCHEMA
Module: Pydantic

Example:
what we expect from the user: title str, content str

### CRUD Operations
Create -> POST  
Read -> GET  
Update -> PUT/PATCH  
Delete -> DELETE

**Best practice and Naming convention** : always use the path plurals e.g posts(v) not post(x)


### To run the applications
```
fastapi dev .\app\main.py
```
or

```
uvicorn app.main:app --reload
```

## Databases
Database management system, software that bridges the database and the client. 
The cilent does not interact with the database directly.

Structured Query Language -> language used to communicate with a DBMS