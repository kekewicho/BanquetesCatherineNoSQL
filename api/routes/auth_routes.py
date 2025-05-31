from flask import Blueprint, request, jsonify, session
from models.User import User # Assuming User.py defines User and its subclasses
from config.conexion_mongo import db # Your MongoDB connection
from werkzeug.security import check_password_hash, generate_password_hash # For password handling

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('usuario') or not data.get('password'):
        return jsonify({"mensaje": "Usuario y contraseña requeridos", "exito": False}), 400

    user_doc = db.usuarios.find_one({"usuario": data['usuario']})

    if user_doc and (user_doc['password'] == data['password']):
        # Passwords match
        user_obj = User(**user_doc) # Create User instance
        session['user'] = user_obj.json() # Store user data in session, using model's json()
        
        # The README response example for login
        login_response = {
            "mensaje": "Login exitoso",
            "exito": True,
            "usuario": {
                "id": str(user_obj._id), # Ensure ID is string
                "usuario": user_obj.usuario,
                "role": user_obj.role.upper(), # Match example "CLIENTE"
                "nombre": user_obj.nombre
            }
        }
        # If role is cliente, add apellido etc.
        if user_obj.role == 'cliente' and hasattr(user_obj, 'apellido'):
             login_response["usuario"]["nombre"] = f"{user_obj.nombre} {getattr(user_obj, 'apellido', '')}".strip()


        return jsonify(login_response), 200
    else:
        return jsonify({"mensaje": "Credenciales inválidas", "exito": False}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logout successful"}), 200 #

# Example: A registration route (optional, not in README but often useful)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('usuario') or not data.get('password') or not data.get('nombre') or not data.get('role'):
        return jsonify({"mensaje": "Faltan campos requeridos (usuario, password, nombre, role)", "exito": False}), 400

    if db.usuarios.find_one({"usuario": data['usuario']}):
        return jsonify({"mensaje": "El nombre de usuario ya existe", "exito": False}), 409

    hashed_password = generate_password_hash(data['password'])
    
    user_data = {
        "usuario": data['usuario'],
        "password": hashed_password,
        "nombre": data['nombre'],
        "role": data['role'].lower() # Store roles consistently, e.g., lowercase
    }
    # Add role-specific fields if provided (e.g., for Cliente)
    if data['role'].lower() == 'cliente':
        user_data["apellido"] = data.get("apellido")
        user_data["telefono"] = data.get("telefono")
        user_data["rfc"] = data.get("rfc")
        user_data["direccion"] = data.get("direccion")
    
    # Here, you might want to use the specific model (User, Cliente, Gerente) to save
    # For simplicity, directly inserting. Ideally, use model.save()
    try:
        new_user = User(**user_data) # Or Cliente(**user_data) if role is 'cliente'
        inserted_id = new_user.save()
        return jsonify({"mensaje": "Usuario registrado exitosamente", "id": str(inserted_id), "exito": True}), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error al registrar usuario: {str(e)}", "exito": False}), 500