from typing import Optional
from fastapi import FastAPI, status, HTTPException
import asyncio
from pydantic import BaseModel,Field,EmailStr
from typing import List

app= FastAPI(

#Personalizar
title = 'API Biblioteca',

description='Ive Martinez- Control de biblioteca',
version='1.0'
)



#BD 
libros = [
    {"id":1,"titulo":"Hábitos atómicos","autor":"James Clear","editorial":"Avery","anio":2018,"paginas":320,"estado":"disponible"},
    {"id":2,"titulo":"Sapiens : De animales a dioses","autor":"Yuval Noah","editorial":"Harper","anio":2011,"paginas":498,"estado":"disponible"},
    {"id":3,"titulo":"Clean Code","autor":"Robert C. Martin","editorial":"Prentice Hall","anio":2008,"paginas":464,"estado":"disponible"},
    {"id":4,"titulo":"The Pragmatic Programmer","autor":"Andrew Hunt","editorial":"Addison","anio":1999,"paginas":352,"estado":"disponible"},
]




#Validaciones
class LibroBase(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de libro", example=1)
    titulo:str = Field(...,min_length=2, max_length=150, description="Nombre del libro")
    autor:str = Field(...,min_length=5, max_length=150, description="Nombre del autor")
    anio: int = Field(..., ge=1451, le=2026, description="Año de publicación" )
    paginas: int = Field(...,ge=1)
    
class Usuario(BaseModel):
    nombre:str = Field(...,min_length=30, max_length=50, description="Nombre del usuario")
    correo: EmailStr
        
class Prestamo(BaseModel):
    id:int = Field(..., gt=0)
    libro_id: int
    usuario: Usuario
    
prestamos: List[dict] = []
#Endpoints

@app.post("/v1/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro:LibroBase):
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(
                status_code=400,
                detail="Libro en existencia"
            )
    libros.append(libro.model_dump())
    return libro

@app.get("/v1/libros")
def listar_libros():
    return libros

@app.get("/v1/libros/buscar/{nombre}")
def buscar_por_nombre(nombre: str):
    resultado = [l for l in libros if nombre.lower() in l["titulo"].lower()]
    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )
    return resultado

@app.post("/v1/prestamos", status_code=status.HTTP_201_CREATED)
def registrar_prestamo(prestamo: Prestamo):
    for l in libros:
        if l["id"] == prestamo.libro_id:
            if l["estado"] == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="Libro prestado"
                )
            l["estado"] = "prestado"
            prestamos.append(prestamo.model_dump())
            return {"mensaje": "Registro de prestamo, correcto"}

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )

@app.put("/v1/prestamos/devolver/{libro_id}")
def devolver_libro(libro_id: int):
    for l in libros:
        if l["id"] == libro_id:
            if l["estado"] == "disponible":
                raise HTTPException(
                    status_code=409,
                    detail="El libro no está prestado"
                )
            l["estado"] = "disponible"
            return {"mensaje": "Libro devuelto correctamente"}

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )

@app.delete("/v1/prestamos/{libro_id}")
def eliminar_prestamo(libro_id: int):
    for p in prestamos:
        if p["libro_id"] == libro_id:
            prestamos.remove(p)
            return {"mensaje": "Registro de préstamo eliminado"}

    raise HTTPException(
        status_code=409,
        detail="No existe el registro"
    )
