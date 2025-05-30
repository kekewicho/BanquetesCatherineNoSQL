# controller/UsuarioController.py
from flask import Blueprint, request, jsonify
from service.UsuarioService import UsuarioService

usuario_bp = Blueprint("usuario_bp", __name__, url_prefix="/usuarios")

@usuario_bp.route("", methods=["POST"])
def crearUsuario():
    data = request.get_json(force=True)
    response, status = UsuarioService.registrar(data)
    return jsonify(response), status

@usuario_bp.route("", methods=["GET"])
def listarUsuarios():
    usuarios = UsuarioService.listarUsuarios()
    return jsonify(usuarios), 200

@usuario_bp.route("/login", methods=["POST"])
def loginUsuario():
    data = request.get_json(force=True)
    correo = data.get("correo") or data.get("usuario")
    password = data.get("password")

    if not correo or not password:
        return {"error": "Faltan Datos"}, 400
    
    return UsuarioService.login(correo, password)

@usuario_bp.route("/<id>", methods=["DELETE"])
def eliminarUsuario(id):
    response, status = UsuarioService.darDeBaja(id)
    return jsonify(response), status