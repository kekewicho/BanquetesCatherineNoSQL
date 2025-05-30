from dataclasses import dataclass
from bson import ObjectId
from api.model.User import User
from api.model.Salon import Salon

@dataclass(kw_only=True)
class Ingrediente:

    descripcion: str
    unidad: str

    __collection__ = "ingredientes"

@dataclass(kw_only=True)
class Platillo:

    nombre: str
    descripcion: str
    tipo_platillo: str
    precio: float
    thumbnail: str
    ingredientes: list[dict]

    __collection__ = "platillos"

@dataclass(kw_only=True)
class Evento:

    fecha: str
    tipo: str
    descripcion: str
    menu: list[dict | Platillo]
    plantilla: list[dict | User]
    salon: dict | Salon
    invitados: list[dict]
    validated: bool

    __collection__ = "eventos"