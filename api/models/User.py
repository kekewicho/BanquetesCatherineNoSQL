from dataclasses import dataclass
from bson import ObjectId
from models.Base import Base

@dataclass(kw_only=True)
class User(Base):

    usuario: str
    password: str
    role: str
    nombre: str

    _id: ObjectId|str = None


    __collection__ = "usuarios"


@dataclass(kw_only=True)
class Cliente(User):

    apellido: str = None
    telefono: str = None
    rfc: str = None
    direccion: None




@dataclass(kw_only=True)
class Gerente(User):

    # Llave foránea hacia los salones
    salon: str | ObjectId