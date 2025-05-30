from dataclasses import dataclass
from bson import ObjectId

@dataclass(kw_only=True)
class Salon:

    nombre: str
    descripcion: str
    capacidad: int

    __collection__ = "salones"