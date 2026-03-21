from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion




router= APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]
)


@router.get("/")
async def consultarUsuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios 
    }
    
    
@router.get("/", status_code=status.HTTP_201_CREATED)
async def agregarUsuarios(usuario:UsuarioBase):
    for usr in usuarios:    