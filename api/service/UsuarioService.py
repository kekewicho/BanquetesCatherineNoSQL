from config.conexion_mongo import db
from model.User import Cliente, Gerente, User

class UsuarioService:

    @staticmethod
    def registrar_usuario(data: dict):
        role = data.get("role")

        if role == "CLIENTE":
            usuario = Cliente(**data)
        elif role.startswith("GERENTE"):
            usuario = Gerente(**data)
        else:
            usuario = User(**data)

        coleccion = db[usuario.__collection__]

        if coleccion.find_one({"usuario": usuario.usuario}):
            return {"error": "Usuario ya existe"}, 400

        coleccion.insert_one(usuario.to_dict())
        return {"mensaje": "Usuario registrado"}, 201
    
    @staticmethod
    def listar_usuarios():
        usuarios = list(db[User.__collection__].find({}, {"_id": 0}))
        return usuarios
