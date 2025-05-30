from dataclasses import dataclass
from bson import ObjectId

@dataclass(kw_only=True)
class Delivery:

    ingredientes: list[dict]
    fecha_creacion: str
    fecha_entrega: str

    __collection__ = "procurement"