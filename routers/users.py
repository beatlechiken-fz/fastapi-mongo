from fastapi import APIRouter, HTTPException
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.db_connection import db_client
from bson import ObjectId

router = APIRouter(prefix="/users",
                   tags=["users"])


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

@router.get("/{id}")
async def user(id:str):
    return searchUser("_id", ObjectId(id))    

'''
@router.get("/")
async def user(id:str):
    return filterUser(id)
'''

@router.post("/", response_model=User, status_code=201)
async def createUser(user:User):
    if type(searchUser("email", user.email)) == User:
        raise HTTPException(status_code=404, detail="Ya existe un usuario con el email especificado")    

    user_dict = dict(user)
    del user_dict["id"]

    _id = db_client.users.insert_one(user_dict).inserted_id
    user_inserted = user_schema(db_client.users.find_one({"_id":_id}))

    return User(**user_inserted)
    
@router.put("/", response_model=User)
async def updateUser(user:User):
    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:    
        raise HTTPException(status_code=404, detail="Ocurrio un error al actualizar el usuario")
    
    return searchUser("_id", ObjectId(user.id))

@router.delete("/{id}", status_code=204)
async def deleteUser(id:str):
    user_deleted = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not user_deleted:
        raise HTTPException(status_code=404, detail="Ocurrio un error al eliminar el usuario")
    
    
def searchUser(key:str, value):
    try:
        user = user_schema(db_client.users.find_one({key:value}))
        return User(**user)
    except:
        return {"Error": "No se encontró el usuario"}