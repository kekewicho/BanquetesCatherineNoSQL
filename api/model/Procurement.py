from dataclasses import dataclass
from bson import ObjectId
from model.Base import Base

@dataclass(kw_only=True)
class Delivery(Base):

    ingredientes: list[dict]
    fecha_creacion: str
    fecha_entrega: str

    __collection__ = "procurement"