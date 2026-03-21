from pydantic import BaseModel,Field

class UsuarioBase(BaseModel):
    id:int = Field(...,gt=0, desription="Identificador de usuarios",example="1")
    nombre:str = Field(...,min_length=30, max_length=50, description="Nombre del usuario")
    edad:int = Field(...,ge=0,le=121, description="Edad válida entre 0 y 121")