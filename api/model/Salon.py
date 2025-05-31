from dataclasses import dataclass
from bson import ObjectId
from model.Base import Base

@dataclass(kw_only=True)
class Salon(Base):

    nombre: str
    descripcion: str
    capacidad: int

    __collection__ = "salones"