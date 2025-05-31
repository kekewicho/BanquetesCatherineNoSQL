from flask import Blueprint, request, jsonify
from service.PlatilloService import PlatilloService

platillo_bp = Blueprint("platillo_bp", __name__, url_prefix="/platillo")

# Crear un nuevo ingrediente
@platillo_bp.route("/ingrediente", methods=["POST"])
def agregarIngrediente():
    data = request.get_json(force=True)
    response, status = PlatilloService.nuevoIngrediente(data)
    return jsonify(response), status

# Eliminar un ingrediente por su ID
@platillo_bp.route("/ingrediente/<string:_id>", methods=["DELETE"])
def eliminarIngrediente(_id):
    response, status = PlatilloService.eliminarIngrediente(_id)
    return jsonify(response), status

# Crear un nuevo platillo
@platillo_bp.route("", methods=["POST"])
def crearPlatillo():
    data = request.get_json(force=True)
    response, status = PlatilloService.nuevoPlatillo(data)
    return jsonify(response), status

# Eliminar un platillo por su ID
@platillo_bp.route("/<string:_id>", methods=["DELETE"])
def eliminarPlatillo(_id):
    response, status = PlatilloService.eliminarPlatillo(_id)
    return jsonify(response), status
