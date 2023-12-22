from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oAuth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "marioferreyra": {
        "username": "marioferreyra",
        "fullname": "Mario Ferreyra",
        "email": "mferreyraz@gmail.com",
        "disabled": False,
        "password": "12345"
    },
    "nayr": {
        "username": "nayr",
        "fullname": "Nayeli Rodríguez",
        "email": "nayr@gmail.com",
        "disabled": False,
        "password": "abcde"
    },
    "anah": {
        "username": "anah",
        "fullname": "Ana Hataway",
        "email": "anah@gmail.com",
        "disabled": True,
        "password": "54321"
    }
}

def getUserDB(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def getUser(username: str):
    if username in users_db:
        return User(**users_db[username])

    
async def currentUser(token: str = Depends(oAuth2)):
    user = getUser(token)

    if not user:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    return user
    

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    is_user_db = users_db.get(form.username)
    if not is_user_db:
        raise HTTPException(status_code=404, detail="No existe el usuario")
    
    user = getUserDB(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=404, detail="Credenciales incorrectas")
    
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/perfil")
async def perfil(user: User = Depends(currentUser)):
    return user
