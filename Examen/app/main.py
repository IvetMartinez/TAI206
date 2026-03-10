
from typing import Optional
from fastapi import FastAPI, status, HTTPException,Depends
import asyncio
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app= FastAPI(
title = 'API de Sistema de citas',
)

citas=[
    {"id":1,"nombre":"Ive", "anio":2026,"estado":"confirmada"},
    {"id":2,"nombre":"Axel", "anio":2026,"estado":"confirmada"},
]

security = HTTPBasic()



#Modelo de validación Pydantic
class CitaBase(BaseModel):
    id:int = Field(...,gt=0, desription="Identificador de usuarios",example="1")
    nombre:str = Field(...,min_length=5, max_length=50, description="Nombre del usuario")
    fecha:int = Field(..., ge=1451, le=2026, description="Año de publicación" )
    motivo:str =Field(...,min_length=5, max_length=100, description="Motivo de cita")


def verificar_peticion(credentials: HTTPBasicCredentials=Depends(security)):
    usuarioAuth=secrets.compare_digest(credentials.username, "root")
    contraAuth=secrets.compare_digest(credentials.password, "1234")
    
    if not(usuarioAuth and contraAuth):
        raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales no validas",
            )
            
            
    return credentials.username


#CREAR CITAS
@app.post("/v1/citas", tags=['CRUD citas'])
async def agregarCitas(cita:CitaBase):
    for cit in citas:
        if cit["id"] == cita.id :
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
            
    citas.append(cita)
    return{
        "mensaje" : "Cita Agregada",
        "datos" : cita,
        "status" : "200"
    }
    
#LISTAR CITAS
@app.get("/v1/citas", tags=['CRUD citas'])
async def consultaCitas():
    return{
        "status":"200",
        "total": len(citas),
        "data":citas
    }
    
#CONSULTAR POR ID
@app.get("/v1/citas/{id}", tags=['Parametro obligatorio'])
async def consultaCitas(id:int): 
    return {"Cita encontrada":id}

#CONFIRMAR CITAS
@app.put("/v1/confirmar/{id}")
def confirmarCita(id: int):
    for l in citas:
        if l["id"] == id:
            if l["estado"] == "confirmado":
                raise HTTPException(
                    status_code=409,
                    detail="La cita esta confirmada"
                )
            l["estado"] = "disponible"
            return {"mensaje": "Libro devuelto correctamente"}

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )

#ACTUALIZAR
@app.put("/v1/citas/{id}", tags=['CRUD citas'])
async def actualizarCita(id: int, cita: dict):

    for cit in citas:
        if cit["id"] == id:
            cit.update(cita)
            return {
                "mensaje": "Cita actualizada",
                "datos": cit,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Cita no encontrada"
    )

#DELETE
@app.delete("/v1/citas/{id}", tags=['CRUD citas'], status_code=status.HTTP_200_OK)
async def eliminarCita(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    for cit in citas:
        if cit["id"] == id:
            citas.remove(cit)
            return {
                "mensaje": f"Cita eliminada correctamente por {usuarioAuth}"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cita no encontrada"
    )
