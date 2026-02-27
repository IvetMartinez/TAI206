#Práctica 1
#importaciones
from typing import Optional
from fastapi import FastAPI, status, HTTPException   
import asyncio   
from pydantic import BaseModel,Field


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

#Modelo de validación Pydantic
class UsuarioBase(BaseModel):
    id:int = Field(...,gt=0, desription="Identificador de usuarios",example="1")
    nombre:str = Field(...,min_length=30, max_length=50, description="Nombre del usuario")
    edad:int = Field(...,ge=0,le=121, description="Edad válida entre 0 y 121")


#Endpoints 
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
async def actualizarUsuario(id: int, usuario: dict):

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

@app.delete("/v1/usuarios/{id}", tags=['CRUD usuarios'])
async def eliminarUsuario(id: int):

    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado",
                "datos": usr,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
