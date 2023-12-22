from pydantic import BaseModel

class User(BaseModel):
    id: str = None
    username: str
    email: str

{
  "username":"Ana", 
  "email":"anahat@gmail.com"
}