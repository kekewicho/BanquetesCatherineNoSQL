from config.conexion_mongo import db
from model.User import Cliente, Gerente, User
from bson import ObjectId

class UsuarioService:

    @staticmethod
    def registrar(data: dict):
        role = data.get("role")

        if role == "CLIENTE":
            usuario = Cliente(**data)
        elif role.startswith("GERENTE"):
            usuario = Gerente(**data)
        elif role.startswith("COLABORADOR"):
            usuario = User(**data)

        usuario.save()
        

        return {"mensaje": "Usuario registrado"}, 201
    
    @staticmethod
    def darDeBaja(_id: str):
        try:
            objectId = ObjectId[_id]
        except:
            return {"error": "ID no valido"}
        
        coleccion = db[User.__collection__]
        resultado = coleccion.delete_one({"_id": objectId})

        if resultado.deleted_count == 0:
            return {"error": "Usuario no encontrado"}, 404
        
        return {"mensaje": "Usuario eliminado"}
    
    @staticmethod
    def listarUsuarios():
        usuarios = list(db[User.__collection__].find({}, {"_id": 0}))
        return usuarios
    
    @staticmethod
    def login(correo: str, password: str):
        coleccion = db[User.__collection__]
        usuario = coleccion.find_one({"usuario": correo})

        if not usuario:
            return {"error": "Usuario no encontrado"}, 400
        
        if usuario["password"] != password:
            return {"error": "Contraseña Incorrecta"}, 400
        
        return {
            "mensaje": "Login exitoso",
            "exito": True,
            "usuario": {
                "id": usuario["_id"],
                "usuario": usuario["usuario"],
                "role": usuario["role"],
                "nombre": usuario["nombre"]
            }
        }, 200
