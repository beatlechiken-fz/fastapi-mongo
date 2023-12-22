from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
SECRET = "Alucard"
ACCESS_TOKEN_DURATION = 10

router = APIRouter()

oAuth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$SQPCwLkUSDnytOM9BjjzH.41VuF0boRn9/JKFUtMlKUKUoRoWeh/S"
    },
    "nayr": {
        "username": "nayr",
        "fullname": "Nayeli Rodríguez",
        "email": "nayr@gmail.com",
        "disabled": False,
        "password": "$2a$12$wu49.iQ/XZrEemxHL2rYAObfWF6Hzl/cHenAq1LOwMp/ozK7jO5MO"
    },
    "anah": {
        "username": "anah",
        "fullname": "Ana Hataway",
        "email": "anah@gmail.com",
        "disabled": True,
        "password": "$2a$12$zqPTUT.5hEicNzoJwlMSZeoz5jlItyH0.WQqZ0dVxaDrFUmhW5Rei"
    }
}


def getUser(username: str):
    if username in users_db:
        return User(**users_db[username])


def getUserDB(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

async def authUser(token: str = Depends(oAuth2)):
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return getUser(username)
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    

async def currentUser(user: User = Depends(authUser)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    is_user_db = users_db.get(form.username)
    if not is_user_db:
        raise HTTPException(status_code=404, detail="No existe el usuario")
    
    user = getUserDB(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=404, detail="Credenciales incorrectas")
    
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/perfil")
async def perfil(user: User = Depends(currentUser)):
    return user