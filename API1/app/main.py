from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi.exceptions import HTTPException
from jose import jwt

app = FastAPI(
    title="API repaso")
#Variable que se declara para el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users = {
    "ivet": {"username":"ivet","email":"ivemart@gmail.com","password":"ive650"},
    "alo": {"username":"alo","email":"alo@gmail.com","password":"alo123"},
    
}

def  encode_token(payload: dict) -> str:
    token = jwt.encode(payload, "my-secret", algorithm="HS256")
    return token

def decode_token(token: Annotated[str,Depends(oauth2_scheme)])-> dict:
    data = jwt.decode(token, "my-secret", algorithms=["HS256"])
    user = users.get(data["username"])
    return user
    
#Endpoint que genera el token
@app.post("/token")
def  login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    user = users.get(form_data.username)
    
    if not user or  form_data.password !=user["password"]:
        
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = encode_token({"username": user["username"], "email": user["email"]})
    return {"access_token": token}


#Cuando se utiliza FormDATA se instala una dependencia  pip install python-multipart

@app.get("/users/profile")
def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user
