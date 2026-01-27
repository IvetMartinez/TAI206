#importaciones
from fastapi import FastAPI

#Inicialización
app= FastAPI()

#Endpoints 
@app.get("/")
async def Holamundo():
    return {"mensaje":"Hola mundo FASTAPI"}


@app.get("/bienvenidos")
async def Bienvenidos():
    return {"mensaje":"Bienvenido a tu API REST"}