from dataclasses import dataclass
from bson import ObjectId
from model.User import User
from model.Salon import Salon
from model.Base import Base


@dataclass(kw_only=True)
class Ingrediente(Base):

    descripcion: str
    unidad: str

    __collection__ = "ingredientes"

@dataclass(kw_only=True)
class Platillo(Base):

    nombre: str
    descripcion: str
    tipo_platillo: str
    precio: float
    thumbnail: str
    ingredientes: list[dict]
    # [{
    # ingrediente: OID(tal),
    # qty: 3
    # }]

    __collection__ = "platillos"

@dataclass(kw_only=True)
class Evento(Base):

    fecha: str
    tipo: str
    descripcion: str
    menu: list[str|ObjectId]
    plantilla: list[str|ObjectId]
    salon: str | ObjectId
    invitados: int
    validated: bool

    __collection__ = "eventos"