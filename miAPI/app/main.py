#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, misc


#Inicializacion 
app= FastAPI(
    title= 'Mi primer API',
    description= 'Ive Martinez',
    version= '1.0'
)

app.include_router(usuarios.router)
app.include_router(misc.router)