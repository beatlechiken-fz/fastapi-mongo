from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/products",
                   tags=["products"])

class Product(BaseModel):
    id: str
    name: str
    detail: str
    price: float

productList = [Product(id="1", name="SSD", detail="SSD M2 480GB", price=405.50),
            Product(id="2", name="Display", detail="15 pulgadas Lenovo", price=1300.00)]

@router.get("/")
async def products():
    return productList

@router.get("/{id}")
async def product(id:str):
    return filterProduct(id)    

'''
@router.post("/", response_model=User, status_code=201)
async def createUser(user:User):
    if type(filterUser(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
    userList.append(user)
    return user
    
@router.put("/", response_model=User)
async def updateUser(user:User):
    for index, userElement in enumerate(userList):
        if userElement.id == user.id:
            userList[index] = user
            return user
    
    raise HTTPException(status_code=404, detail="No se encontró el usuario a actualizar")
    

@router.delete("/{id}")
async def deleteUser(id:str):
    for index, userElement in enumerate(userList):
        if userElement.id == id:
            del userList[index] 
            return {"Ok": "Se elimino el usuario"}
    
    raise HTTPException(status_code=404, detail="No se encontró el usuario a eliminar")
''' 
        
def filterProduct(id:int):
    try:
        return list(filter(lambda product: product.id == id, productList))[0]
    except:
        raise HTTPException(status_code=404, detail="No se encontró el producto")