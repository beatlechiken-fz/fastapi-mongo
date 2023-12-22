from fastapi import FastAPI
from routers import users, products, auth_jwt

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth_jwt.router)

@app.get("/")
async def root():
    return {"Hola": "FastAPI"}

