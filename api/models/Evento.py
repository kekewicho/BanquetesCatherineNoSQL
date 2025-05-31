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
class TempPlatilloForEnrich(Base): # Temporary for showing enrichment structure
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
class Evento(Base): #
    fecha: str
    tipo: str
    descripcion: str
    menu: list[str|ObjectId] # List of Platillo ObjectIds
    plantilla: list[str|ObjectId] # List of User (staff) ObjectIds
    salon: str | ObjectId # Salon ObjectId
    invitados: int
    validated: bool
    cliente_id: str | ObjectId = None # Added based on README examples

    _id = str | ObjectId = None

    __collection__ = "eventos"

    def json(self, enrich=True):
        # Get the basic dictionary with ObjectIds converted to strings
        data = super().json() # Base.json() handles __remove_oid

        if enrich:
            # Enrich Salon
            if data.get('salon') and isinstance(self.salon, (str, ObjectId)):
                salon_doc = db[Salon.__collection__].find_one({'_id': ObjectId(self.salon)})
                data['salon'] = Salon(**salon_doc).json() if salon_doc else None

            # Enrich Menu (Platillos)
            if data.get('menu') and self.menu:
                enriched_menu_list = []
                for p_id in self.menu: # self.menu should be list of ObjectIds or strs
                    p_doc = db[TempPlatilloForEnrich.__collection__].find_one({'_id': ObjectId(p_id)})
                    if p_doc:
                        # Use the Platillo's own json method, assuming it also enriches its ingredients
                        enriched_menu_list.append(TempPlatilloForEnrich(**p_doc).json(enrich_ingredients=True))
                data['menu'] = enriched_menu_list
            
            # Enrich Plantilla (Staff - Users)
            if data.get('plantilla') and self.plantilla:
                enriched_plantilla_list = []
                for staff_id in self.plantilla:
                    staff_doc = db[User.__collection__].find_one({'_id': ObjectId(staff_id)})
                    if staff_doc:
                        # Selectively return fields for staff display
                        enriched_plantilla_list.append({
                            "_id": str(staff_doc["_id"]),
                            "nombre": staff_doc.get("nombre"),
                            "usuario": staff_doc.get("usuario"),
                            "role": staff_doc.get("role")
                        })
                data['plantilla'] = enriched_plantilla_list

            # Enrich Cliente
            if data.get('cliente_id') and self.cliente_id:
                # Ensure __collection__ is set in Cliente or User if it's a shared collection
                client_doc = db[User.__collection__].find_one({'_id': ObjectId(self.cliente_id), 'role': 'cliente'})
                if client_doc:
                    data['cliente'] = Cliente(**client_doc).json()
                # data.pop('cliente_id', None) # Optional: remove after enriching
        return data
