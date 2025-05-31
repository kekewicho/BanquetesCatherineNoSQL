from config.conexion_mongo import db
from bson import ObjectId
from model.Evento import Evento

class EventoService:

    @staticmethod
    def nuevoEvento(data: dict):
        try:
            coleccion = db[Evento.__collection__]
            resultado = coleccion.insert_one(data)
            return {"mensaje": "Evento creado", "id": str(resultado.inserted_id)}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def modificarPlantilla(evento_id: str, nueva_plantilla: list):
        try:
            coleccion = db[Evento.__collection__]
            result = coleccion.update_one(
                {"_id": ObjectId(evento_id)},
                {"$set": {"plantilla": nueva_plantilla}}
            )
            if result.matched_count == 0:
                return {"error": "Evento no encontrado"}, 404
            return {"mensaje": "Plantilla actualizada correctamente"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def eliminarEvento(evento_id: str):
        try:
            coleccion = db[Evento.__collection__]
            result = coleccion.delete_one({"_id": ObjectId(evento_id)})
            if result.deleted_count == 0:
                return {"error": "Evento no encontrado"}, 404
            return {"mensaje": "Evento eliminado correctamente"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        

