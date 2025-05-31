from dataclasses import dataclass
from bson import ObjectId
from models.Base import Base

@dataclass(kw_only=True)
class Salon(Base):

    nombre: str
    descripcion: str
    capacidad: int
    _id: ObjectId | str = None

    __collection__ = "salones"