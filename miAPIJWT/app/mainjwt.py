#Práctica 1
#importaciones
from typing import Optional
from fastapi import FastAPI, status, HTTPException,Depends
import asyncio   
from pydantic import BaseModel,Field
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


# CONFIGURACION JWT
SECRET_KEY = "mi_clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Inicialización
app= FastAPI(

#Personalizar 
title = 'Mi primer API',
description='Ive Martinez',
version='1.0'
)
#Práctica 2: Simulación de Base de datos

usuarios=[
    {"id":1,"nombre":"Ive", "edad":22},
    {"id":2,"nombre":"Axel", "edad":35},
    {"id":3,"nombre":"Ivi", "edad":20},
]

def crear_token_acceso(data: dict, expires_delta: timedelta | None = None):
    
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#Modelo de validación Pydantic
class UsuarioBase(BaseModel):
    
    id:int = Field(...,gt=0, desription="Identificador de usuarios",example="1")
    nombre:str = Field(...,min_length=30, max_length=50, description="Nombre del usuario")
    edad:int = Field(...,ge=0,le=121, description="Edad válida entre 0 y 121")


#Endpoints

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    username = form_data.username
    password = form_data.password

    if username != "admin" or password != "123456":
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    access_token_expires = timedelta(minutes=30)

    access_token = crear_token_acceso(
        data={"sub": username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
    

async def validar_token(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return username

@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje":"Hola mundo FASTAPI"}


@app.get("/V1/bienvenidos", tags=['Inicio'])
async def bienvenidos():
    return {"mensaje":"Bienvenido a tu API REST"}


#Práctica 2

#Se crea un nuevo endpoint
@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(5) #No es obligatorio es una simulación de tiempo de espera 
    return {"mensaje":"Tu calificación en TAI es 10"}


#Definir parametros obloigatorios mediante las llaves

@app.get("/v1/parametroO/{id}", tags=['Parametro obligatorio'])
async def consultaUsuarios(id:int): 
    return {"Usuario encontrado":id}

@app.get("/v1/parametroOp", tags=['Parametro opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]== id:
                return {"Usuario encontrado":id,
                        "Usuario":usuario}
            
        return {"Usuario  no encontrado"}
    else:
        return{"AVISO": "No se proporciono id"}
    
    
    
    #seguimiento de la practica 3 
    
@app.get("/v1/usuarios", tags=['CRUD usuarios'])
async def consultaUsuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
    
    
@app.post("/v1/usuarios", tags=['CRUD usuarios'])
async def agregarUsuarios(usuario:UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id :
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
            
    usuarios.append(usuario)
    return{
        "mensaje" : "Usuario Agregado",
        "datos" : usuario,
        "status" : "200"
    }
    
@app.put("/v1/usuarios/{id}", tags=['CRUD usuarios'])
async def actualizarUsuario(id: int, usuario: dict, token:str = Depends(validar_token)):

    for usr in usuarios:
        if usr["id"] == id:
            usr.update(usuario)
            return {
                "mensaje": "Usuario actualizado",
                "datos": usr,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/{id}", tags=['CRUD usuarios'], status_code=status.HTTP_200_OK)
async def eliminarUsuario(id: int, token: str = Depends(validar_token)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado correctamente por {usuarioAuth}"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )
