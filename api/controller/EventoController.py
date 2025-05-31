from flask import Blueprint, request, jsonify
from service.EventoService import EventoService

evento_bp = Blueprint("evento_bp", __name__, url_prefix="/evento")

# Crear un nuevo evento
@evento_bp.route("", methods=["POST"])
def crearEvento():
    data = request.get_json(force=True)
    response, status = EventoService.nuevoEvento(data)
    return jsonify(response), status

# Modificar solo la plantilla de un evento
@evento_bp.route("/<string:evento_id>/plantilla", methods=["PUT"])
def modificarPlantilla(evento_id):
    data = request.get_json(force=True)
    nueva_plantilla = data.get("plantilla")
    if not nueva_plantilla:
        return {"error": "Falta la plantilla"}, 400
    response, status = EventoService.modificarPlantilla(evento_id, nueva_plantilla)
    return jsonify(response), status

# Eliminar un evento
@evento_bp.route("/<string:evento_id>", methods=["DELETE"])
def eliminarEvento(evento_id):
    response, status = EventoService.eliminarEvento(evento_id)
    return jsonify(response), status