from dataclasses import dataclass
from bson import ObjectId
from models.User import User
from models.Salon import Salon
from models.Base import Base
from config.conexion_mongo import db
from dataclasses import field
from models.User import Cliente


@dataclass(kw_only=True)
class Ingrediente(Base):

    _id: ObjectId | str = None
    descripcion: str
    unidad: str

    __collection__ = "ingredientes"

@dataclass(kw_only=True)
class Platillo(Base):

    _id: ObjectId | str = None
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
class TempPlatilloForEnrich(Base): 
    nombre: str = ""
    descripcion: str = ""
    tipo_platillo: str = ""
    precio: float = 0.0
    thumbnail: str = ""
    ingredientes: list[dict] = field(default_factory=list)
    __collection__ = "platillos"

    def json(self, enrich_ingredients=True):
        data = super().json()
        if enrich_ingredients and self.ingredientes:
            enriched_ings = []
            for ing_item in self.ingredientes:
                ing_id = ing_item.get('ingrediente') # ObjectId in DB
                qty = ing_item.get('qty')
                if ing_id:
                    ing_doc = db.ingredientes.find_one({'_id': ObjectId(ing_id)})
                    if ing_doc:
                        # from models.Evento import Ingrediente # Ensure Ingrediente model is imported
                        enriched_ings.append({
                            "ingrediente": Ingrediente(**ing_doc).json(), # Use Ingrediente's json
                            "qty": qty
                        })
            data['ingredientes'] = enriched_ings
        return data


@dataclass(kw_only=True)
class Evento(Base): 
    _id: ObjectId | str = None
    fecha: str
    tipo: str
    descripcion: str
    menu: list[str | ObjectId] = field(default_factory=list)         # Lista de IDs de platillos
    plantilla: list[str | ObjectId] = field(default_factory=list)    # Lista de IDs de colaboradores
    salon: str | ObjectId = None                                     # ID del salón
    invitados: int = 0
    validated: bool = True
    cliente_id: str | ObjectId = None                                # ID del cliente

    _id: str | ObjectId = None

    __collection__ = "eventos"

    def __post_init__(self):
        if isinstance(self._id, str):
            self._id = ObjectId(self._id)
        if isinstance(self.salon, str):
            self.salon = ObjectId(self.salon)
        if isinstance(self.cliente_id, str):
            self.cliente_id = ObjectId(self.cliente_id)
        self.menu = [ObjectId(p) if isinstance(p, str) else p for p in self.menu]
        self.plantilla = [ObjectId(p) if isinstance(p, str) else p for p in self.plantilla]

    def json(self, enrich=True):
        data = super().json()

        if enrich:
            # Enriquecer salón
            if data.get('salon') and isinstance(self.salon, (str, ObjectId)):
                salon_doc = db[Salon.__collection__].find_one({'_id': ObjectId(self.salon)})
                data['salon'] = Salon(**salon_doc).json() if salon_doc else None

            # Enriquecer menú
            if data.get('menu') and self.menu:
                enriched_menu_list = []
                for p_id in self.menu:
                    p_doc = db[TempPlatilloForEnrich.__collection__].find_one({'_id': ObjectId(p_id)})
                    if p_doc:
                        enriched_menu_list.append(TempPlatilloForEnrich(**p_doc).json(enrich_ingredients=True))
                data['menu'] = enriched_menu_list

            # Enriquecer plantilla (staff)
            if data.get('plantilla') and self.plantilla:
                enriched_plantilla_list = []
                for staff_id in self.plantilla:
                    staff_doc = db[User.__collection__].find_one({'_id': ObjectId(staff_id)})
                    if staff_doc:
                        enriched_plantilla_list.append({
                            "_id": str(staff_doc["_id"]),
                            "nombre": staff_doc.get("nombre"),
                            "usuario": staff_doc.get("usuario"),
                            "role": staff_doc.get("role")
                        })
                data['plantilla'] = enriched_plantilla_list

            if data.get('cliente_id') and self.cliente_id:
                client_doc = db[User.__collection__].find_one({'_id': ObjectId(self.cliente_id), 'role': 'cliente'})
                if client_doc:
                    data['cliente'] = Cliente(**client_doc).json()

        return data
