from dataclasses import dataclass
from bson import ObjectId
from models.Base import Base

@dataclass(kw_only=True)
class Delivery(Base):

    ingredientes: list[dict]
    fecha_creacion: str
    fecha_entrega: str
    _id: str | ObjectId = None


    __collection__ = "procurement"