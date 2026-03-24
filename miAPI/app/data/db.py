from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 1. Definir la URL de conexión
DATABASE_URL= os.getenv(
    "DATABASE_URL","postgresql://admin:123456@postgres:5432/DB_miapi"
)


# 2. Creación del motor de conexión
engine = create_engine(DATABASE_URL)

# 3. Se agrega el gestor de sesiones
sesionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine)

# 4. Base declarativa para modelos
Base = declarative_base()

# 5. Función para el manejo en sessiones en los request
def get_db():
    db = sesionLocal()
    try:
        yield db
    finally:
        db.close()   

