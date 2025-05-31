from config.conexion_mongo import db
from model.Evento import Platillo, Ingrediente
from bson import ObjectId
from dataclasses import asdict

class PlatilloService:

    @staticmethod
    def nuevoIngrediente(data: dict):
        ingrediente = Ingrediente(**data)
        coleccion = db[Ingrediente.__collection__]

        if coleccion.find_one({"descripcion": ingrediente.descripcion}):
            return {"error": "Ingrediente ya existe"}, 400

        coleccion.insert_one(asdict(ingrediente))
        return {"mensaje": "Ingrediente registrado"}, 201

    @staticmethod
    def eliminarIngrediente(_id: str):
        try:
            oid = ObjectId(_id)
        except:
            return {"error": "ID inválido"}, 400

        coleccion = db[Ingrediente.__collection__]
        result = coleccion.delete_one({"_id": oid})

        if result.deleted_count == 0:
            return {"error": "Ingrediente no encontrado"}, 404

        return {"mensaje": "Ingrediente eliminado"}, 200

    @staticmethod
    def nuevoPlatillo(data: dict):
        platillo = Platillo(**data)
        coleccion = db[Platillo.__collection__]

        if coleccion.find_one({"nombre": platillo.nombre}):
            return {"error": "Platillo ya existe"}, 400

        doc = asdict(platillo)

        if doc.get("_id") is None:
            doc.pop("_id")

        coleccion.insert_one(doc)
        return {"mensaje": "Platillo registrado"}, 201


    @staticmethod
    def eliminarPlatillo(_id: str):
        try:
            oid = ObjectId(_id)
        except:
            return {"error": "ID inválido"}, 400

        coleccion = db[Platillo.__collection__]
        result = coleccion.delete_one({"_id": oid})

        if result.deleted_count == 0:
            return {"error": "Platillo no encontrado"}, 404

        return {"mensaje": "Platillo eliminado"}, 200
