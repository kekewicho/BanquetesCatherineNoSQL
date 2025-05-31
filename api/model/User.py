from dataclasses import dataclass, asdict
from bson import ObjectId

@dataclass(kw_only=True)
class User:
    usuario: str
    password: str
    role: str
    nombre: str
    __collection__ = "usuarios"

    def to_dict(self):
        return asdict(self)

@dataclass(kw_only=True)
class Cliente(User):
    apellido: str = None
    telefono: str = None
    rfc: str = None
    direccion: str = None

@dataclass(kw_only=True)
class Gerente(User):
    salon: str | ObjectId
