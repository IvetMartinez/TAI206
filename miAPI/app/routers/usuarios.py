#*************************************************************
# Usuarios CRUD
#*************************************************************
#importaciones 
from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion


from sqlalchemy.orm import Session      #P9
from app.data.db import get_db          #P9
from app.data.usuario import Usuario  as usuarioDB   #P9



router= APIRouter(
    prefix= "/v1/usuarios",
    tags= ["CRUD HTTP"]
)

#Endpoints
@router.get("/")
async def consultaUsuarios(db:Session = Depends(get_db)):  #9
    
    usuarios_db =db.query(usuarioDB).all()
    return{
        "status":"200",
        "total": len(usuarios_db),
        "data":usuarios_db
    }
    
    
@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregarUsuarios(usuarioP:UsuarioBase, db:Session=Depends(get_db)): #Implementamos validadcion pydantic
    
    nuevoUsuario = usuarioDB(nombre= usuarioP.nombre, edad=usuarioP.edad)
    
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)
    
    return{
        "mensaje" : "Usuario Agregado",
        "datos" : nuevoUsuario
    }
    
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizarUsuario(id: int, usuario: dict):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            #Remplazamos completamente el usuario
            usuario["id"] = id
            usuarios[index]=usuario
            return {
                "mensaje": "Usuario actualizado",
                "datos": usuarios[index]
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminarUsuario(id: int, usuarioAuth: str= Depends(verificar_Peticion)):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado correctamente por {usuarioAuth}"
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado para eliminar"
    )
  