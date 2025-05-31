from flask import Blueprint, request, jsonify, session
from models.User import User, Cliente, Gerente 
from models.Evento import Evento, Platillo, Ingrediente 
from models.Salon import Salon 
from models.Procurement import Delivery 
from config.conexion_mongo import db
from bson import ObjectId
from utils.decorators import login_required, roles_required
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from models.Base import Base

from routes.public_routes import enrich_platillo 
from routes.client_routes import enrich_event_details 

banquet_admin_bp = Blueprint('banquet_admin_bp', __name__)

@banquet_admin_bp.route('/user', methods=['POST'])
def agregarStaff():
    data = request.get_json()
    required_fields = ['usuario', 'password', 'role', 'nombre']
    if not all(field in data for field in required_fields):
        return jsonify({"mensaje": "Faltan campos requeridos (usuario, password, role, nombre)"}), 400

    if db.usuarios.find_one({"usuario": data['usuario']}):
        return jsonify({"mensaje": "El nombre de usuario ya existe"}), 409
    
    
    if data.get("role") == "CLIENTE":
        usuario = Cliente(**data)
    elif data.get("role") == "GERENTE":
        usuario = Gerente(**data)
    elif data.get("role") == "COLABORADOR":
        usuario = User(**data)
    
    try:
        usuario.save()
        return jsonify(usuario.json()), 201 
    except Exception as e:
        return jsonify({"mensaje": f"Error al crear empleado: {str(e)}"}), 500

@banquet_admin_bp.route('/staff', methods=['GET'])
def obtenerStaff():
    query = {"role": {"$in": ["GERENTE", "COLABORADOR"]}}

    staff_cursor = db.usuarios.find(query)

    role_class_map = {
        'GERENTE': Gerente,
        'COLABORADOR': User
    }

    staff_list = []
    for s in staff_cursor:
        role = s.get("role", "")
        cls = role_class_map.get(role, User)
        staff_list.append(cls(**s).json())

    return jsonify(staff_list), 200
    
@banquet_admin_bp.route('/staff/<string:staff_id>', methods=['GET'])
def obtenerStaffPorId(staff_id):
    try:
        staff_obj_id = ObjectId(staff_id)
    except Exception:
        return jsonify({"mensaje": "ID de empleado inválido"}), 400

    staff_doc = db.usuarios.find_one({'_id': staff_obj_id})
    if not staff_doc:
        return jsonify({"mensaje": "Empleado no encontrado"}), 404

    role = staff_doc.get("role", "").lower()
    role_class_map = {
        'cliente': Cliente,
        'gerente': Gerente,
        'colaborador': User
    }

    cls = role_class_map.get(role, User)
    return jsonify(cls(**staff_doc).json()), 200

@banquet_admin_bp.route('/staff/<string:staff_id>', methods=['PUT'])
def actualizarStaff(staff_id):
    data = request.get_json()

    try:
        staff_obj_id = ObjectId(staff_id)
    except Exception:
        return jsonify({"mensaje": "ID de empleado inválido"}), 400

    existing_doc = db.usuarios.find_one({'_id': staff_obj_id})
    if not existing_doc:
        return jsonify({"mensaje": "Empleado no encontrado"}), 404

    update_data = {}
    allowed_fields = ['telefono', 'role', 'nombre', 'apellido', 'rfc', 'direccion', 'salon']
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field].lower() if field == 'role' else data[field]

    if not update_data:
        return jsonify({"mensaje": "No hay datos para actualizar"}), 400

    result = db.usuarios.update_one({'_id': staff_obj_id}, {'$set': update_data})

    updated_doc = db.usuarios.find_one({'_id': staff_obj_id})
    role = updated_doc.get("role", "").lower()

    role_class_map = {
        'cliente': Cliente,
        'gerente': Gerente,
        'colaborador': User
    }
    cls = role_class_map.get(role, User)

    return jsonify(cls(**updated_doc).json()), 200 if result.modified_count > 0 else 304

@banquet_admin_bp.route('/staff/<string:staff_id>', methods=['DELETE'])
def eliminarStaff(staff_id):
    try:
        staff_obj_id = ObjectId(staff_id)
    except Exception:
        return jsonify({"mensaje": "ID de empleado inválido"}), 400
    
    
    result = db.usuarios.delete_one({'_id': staff_obj_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Staff removido de manera correcta."}), 200 
    return jsonify({"mensaje": "Empleado no encontrado"}), 404


@banquet_admin_bp.route('/clients', methods=['GET'])
def obtenerClientes():
    query = {'role': 'CLIENTE'}
    search_term = request.args.get('search')
    if search_term:
        
        query['$or'] = [
            {'nombre': {'$regex': search_term, '$options': 'i'}},
            {'apellido': {'$regex': search_term, '$options': 'i'}},
            {'rfc': {'$regex': search_term, '$options': 'i'}},
            {'usuario': {'$regex': search_term, '$options': 'i'}}
        ]
    
    clients_cursor = db.usuarios.find(query)
    clients_list = [Cliente(**c).json() for c in clients_cursor]
    return jsonify(clients_list), 200

@banquet_admin_bp.route('/clients/<string:client_id>', methods=['GET'])
def obtenerClientePorId(client_id):
    try:
        client_obj_id = ObjectId(client_id)
    except Exception:
        return jsonify({"mensaje": "ID de cliente inválido"}), 400
    
    client_doc = db.usuarios.find_one({'_id': client_obj_id, 'role': 'CLIENTE'})
    if client_doc:
        return jsonify(Cliente(**client_doc).json()), 200
    return jsonify({"mensaje": "Cliente no encontrado"}), 404

@banquet_admin_bp.route('/clients/<string:client_id>/events', methods=['GET'])
def obtenerEventosPorCliente(client_id):
    try:
        client_obj_id = ObjectId(client_id)
    except Exception:
        return jsonify({"mensaje": "ID de cliente inválido"}), 400

    if not db.usuarios.find_one({'_id': client_obj_id, 'role': 'cliente'}):
         return jsonify({"mensaje": "Cliente no encontrado"}), 404
         
    
    events_cursor = db.eventos.find({'cliente_id': client_obj_id}).sort("fecha", -1) 
    events_list = [enrich_event_details(e_doc) for e_doc in events_cursor]
    return jsonify(events_list), 200

@banquet_admin_bp.route('/clients', methods=['POST'])
def registrarCliente():
    data = request.get_json()
    required_fields = ['usuario', 'password', 'nombre', 'apellido'] 
    if not all(field in data for field in required_fields):
        return jsonify({"mensaje": "Campos requeridos faltantes"}), 400

    if db.usuarios.find_one({"usuario": data['usuario']}):
        return jsonify({"mensaje": "El nombre de usuario ya existe"}), 409

    hashed_password = generate_password_hash(data['password'])
    client_data_dict = {
        "usuario": data['usuario'],
        "password": hashed_password,
        "role": "cliente",
        "nombre": data['nombre'],
        "apellido": data.get('apellido'),
        "telefono": data.get('telefono'),
        "rfc": data.get('rfc'),
        "direccion": data.get('direccion') 
    }
    
    new_client = Cliente(**client_data_dict)
    try:
        inserted_id = new_client.save()
        created_client_doc = db.usuarios.find_one({'_id': inserted_id})
        return jsonify(Cliente(**created_client_doc).json()), 201 
    except Exception as e:
        return jsonify({"mensaje": f"Error al crear cliente: {str(e)}"}), 500

@banquet_admin_bp.route('/clients/<string:client_id>', methods=['PUT'])
def actualizarCliente(client_id):
    data = request.get_json()
    try:
        client_obj_id = ObjectId(client_id)
    except Exception:
        return jsonify({"mensaje": "ID de cliente inválido"}), 400

    if not db.usuarios.find_one({'_id': client_obj_id, 'role': 'cliente'}):
        return jsonify({"mensaje": "Cliente no encontrado"}), 404

    update_data = {k: v for k, v in data.items() if k not in ['_id', 'usuario', 'password', 'role']}
    if not update_data:
        return jsonify({"mensaje": "No hay datos para actualizar"}), 400

    result = db.usuarios.update_one({'_id': client_obj_id}, {'$set': update_data})
    if result.modified_count > 0:
        updated_client_doc = db.usuarios.find_one({'_id': client_obj_id})
        return jsonify(Cliente(**updated_client_doc).json()), 200
    return jsonify({"mensaje": "No se pudo actualizar o no hubo cambios"}), 304

#Hasta aquí todo bien

@banquet_admin_bp.route('/events', methods=['POST'])
def crearEvento():
    data = request.get_json()
    required_fields = ['fecha', 'tipo', 'descripcion', 'menu', 'plantilla', 'salon', 'invitados', 'cliente_id']
    if not all(field in data for field in required_fields):
        return jsonify({"mensaje": "Faltan campos requeridos"}), 400

    try:
        cliente_obj_id = ObjectId(data['cliente_id'])
        if not db.usuarios.find_one({'_id': cliente_obj_id, 'role': 'CLIENTE'}):
            return jsonify({"mensaje": "Cliente no encontrado"}), 404

        salon_obj_id = ObjectId(data['salon'])
        if not db.salones.find_one({'_id': salon_obj_id}):
            return jsonify({"mensaje": "Salón no encontrado"}), 404

        menu_obj_ids = [ObjectId(pid) for pid in data['menu']]
        if db.platillos.count_documents({'_id': {'$in': menu_obj_ids}}) != len(menu_obj_ids):
            return jsonify({"mensaje": "Uno o más platillos no son válidos"}), 404

        plantilla_obj_ids = [ObjectId(sid) for sid in data['plantilla']]
        colaboradores = db.usuarios.find({'_id': {'$in': plantilla_obj_ids}, 'role': 'COLABORADOR'})
        colaboradores_ids = {c['_id'] for c in colaboradores}
        if len(colaboradores_ids) != len(plantilla_obj_ids):
            return jsonify({"mensaje": "Todos los miembros de la plantilla deben ser COLABORADORES"}), 400

    except Exception as e:
        return jsonify({"mensaje": f"IDs inválidos: {e}"}), 400

    event_data_dict = {
        "fecha": data['fecha'],
        "tipo": data['tipo'],
        "descripcion": data['descripcion'],
        "menu": [str(pid) for pid in menu_obj_ids],
        "plantilla": [str(sid) for sid in plantilla_obj_ids],
        "salon": str(salon_obj_id),
        "invitados": int(data['invitados']),
        "validated": data.get('validated', True),
        "cliente_id": str(cliente_obj_id)
    }

    new_event = Evento(**event_data_dict)
    try:
        inserted_id = new_event.save()
        return jsonify(new_event.json(enrich=True)), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error al crear evento: {str(e)}"}), 500

@banquet_admin_bp.route('/events', methods=['GET'])
def obtenerEventos():
    query = {}
    if request.args.get('from_date'):
        query['fecha'] = {'$gte': request.args.get('from_date')}
    if request.args.get('to_date'):
        query.setdefault('fecha', {})['$lte'] = request.args.get('to_date')
    if request.args.get('salon_id'):
        query['salon'] = ObjectId(request.args.get('salon_id'))
    if request.args.get('validated'):
        query['validated'] = request.args.get('validated').lower() == 'true'
    
    status_filter = request.args.get('status')
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    if status_filter == "upcoming":
        query.setdefault('fecha', {})['$gte'] = current_date_str
    elif status_filter == "past":
        query.setdefault('fecha', {})['$lt'] = current_date_str

    events_cursor = db.eventos.find(query).sort("fecha", 1) 
    events_list = [enrich_event_details(e_doc) for e_doc in events_cursor]
    return jsonify(events_list), 200

@banquet_admin_bp.route('/events/<string:event_id>', methods=['GET'])
def obtenerEventoPorId(event_id): 
    try:
        event_obj_id = ObjectId(event_id)
    except Exception:
        return jsonify({"mensaje": "ID de evento inválido"}), 400
    
    event_doc = db.eventos.find_one({'_id': event_obj_id})
    if event_doc:
        return jsonify(enrich_event_details(event_doc)), 200 
    return jsonify({"mensaje": "Evento no encontrado"}), 404

@banquet_admin_bp.route('/events/<string:event_id>', methods=['PUT'])
def actualizarEvento(event_id):
    data = request.get_json()
    try:
        event_obj_id = ObjectId(event_id)
    except Exception:
        return jsonify({"mensaje": "ID de evento inválido"}), 400

    if not db.eventos.find_one({'_id': event_obj_id}):
        return jsonify({"mensaje": "Evento no encontrado"}), 404

    update_fields = {}
    simple_fields = ['fecha', 'tipo', 'descripcion', 'invitados', 'validated']
    for field in simple_fields:
        if field in data:
            update_fields[field] = data[field]
            if field == 'invitados': update_fields[field] = int(data[field])
            if field == 'validated': update_fields[field] = bool(data[field])

    
    if 'salon' in data:
        update_fields['salon'] = ObjectId(data['salon'])
    if 'menu' in data and isinstance(data['menu'], list):
        update_fields['menu'] = [ObjectId(pid) for pid in data['menu']]
    if 'plantilla' in data and isinstance(data['plantilla'], list):
        update_fields['plantilla'] = [ObjectId(sid) for sid in data['plantilla']]
    if 'cliente_id' in data:
         update_fields['cliente_id'] = ObjectId(data['cliente_id'])


    if not update_fields:
        return jsonify({"mensaje": "No hay datos para actualizar"}), 400

    result = db.eventos.update_one({'_id': event_obj_id}, {'$set': update_fields})
    if result.modified_count > 0:
        updated_event_doc = db.eventos.find_one({'_id': event_obj_id})
        return jsonify(enrich_event_details(updated_event_doc)), 200
    return jsonify({"mensaje": "No se pudo actualizar o no hubo cambios"}), 304

@banquet_admin_bp.route('/events/<string:event_id>', methods=['DELETE'])
def borrarEvento(event_id):
    try:
        event_obj_id = ObjectId(event_id)
    except Exception:
        return jsonify({"mensaje": "ID de evento inválido"}), 400
    
    result = db.eventos.delete_one({'_id': event_obj_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Event deleted successfully."}), 200 
    return jsonify({"mensaje": "Evento no encontrado"}), 404

@banquet_admin_bp.route('/events/<string:event_id>/staff', methods=['GET'])
def obtenerStaffPorEvento(event_id):
    try:
        event_obj_id = ObjectId(event_id)
    except Exception:
        return jsonify({"mensaje": "ID de evento inválido"}), 400
    
    event_doc = db.eventos.find_one({'_id': event_obj_id}, {'plantilla': 1}) 
    if not event_doc or 'plantilla' not in event_doc:
        return jsonify({"mensaje": "Evento no encontrado o sin personal asignado"}), 404

    staff_ids = event_doc.get('plantilla', [])
    staff_list = []
    if staff_ids:
        staff_cursor = db.usuarios.find({'_id': {'$in': staff_ids}})
        staff_list = [User(**s).json() for s in staff_cursor] 
    return jsonify(staff_list), 200

@banquet_admin_bp.route('/events/<string:event_id>/staff', methods=['POST'])
def asignarStaffAEvento(event_id):
    data = request.get_json()
    if 'staff_id' not in data:
        return jsonify({"mensaje": "ID de empleado (staff_id) requerido"}), 400
    
    try:
        event_obj_id = ObjectId(event_id)
        staff_obj_id = ObjectId(data['staff_id'])
    except Exception:
        return jsonify({"mensaje": "IDs inválidos"}), 400

    
    if not db.eventos.find_one({'_id': event_obj_id}):
        return jsonify({"mensaje": "Evento no encontrado"}), 404
    if not db.usuarios.find_one({'_id': staff_obj_id}): 
        return jsonify({"mensaje": "Empleado no encontrado"}), 404

    result = db.eventos.update_one(
        {'_id': event_obj_id},
        {'$addToSet': {'plantilla': staff_obj_id}} 
    )
    if result.modified_count > 0:
        
        updated_event = db.eventos.find_one({'_id': event_obj_id})
        return jsonify(enrich_event_details(updated_event)), 200 
    return jsonify({"mensaje": "Empleado ya asignado o no se pudo asignar"}), 304

@banquet_admin_bp.route('/events/<string:event_id>/staff/<string:staff_id_to_remove>', methods=['DELETE'])
def quitarStaffDeEvento(event_id, staff_id_to_remove):
    try:
        event_obj_id = ObjectId(event_id)
        staff_obj_id_to_remove = ObjectId(staff_id_to_remove)
    except Exception:
        return jsonify({"mensaje": "IDs inválidos"}), 400
        
    result = db.eventos.update_one(
        {'_id': event_obj_id},
        {'$pull': {'plantilla': staff_obj_id_to_remove}}
    )
    if result.modified_count > 0:
        return jsonify({"message": "Staff member removed from event successfully."}), 200 
    return jsonify({"mensaje": "Empleado no encontrado en el evento o no se pudo remover"}), 404

@banquet_admin_bp.route('/procurement/required-ingredients', methods=['GET'])
@roles_required(allowed_roles=['admin_banquetes'])
def get_required_ingredients():
    from_date_str = request.args.get('from_date')
    to_date_str = request.args.get('to_date')

    if not from_date_str or not to_date_str:
        return jsonify({"mensaje": "Parámetros 'from_date' y 'to_date' son requeridos (YYYY-MM-DD)"}), 400


    
    required_map = {}
    events_in_range = db.eventos.find({'fecha': {'$gte': from_date_str, '$lte': to_date_str}})
    for event in events_in_range:
        num_invitados = event.get('invitados', 1)
        for platillo_id in event.get('menu', []):
            platillo = db.platillos.find_one({'_id': ObjectId(platillo_id)})
            if platillo:
                for ing_item in platillo.get('ingredientes', []): 
                    ing_id = ing_item.get('ingrediente')
                    ing_qty_per_platillo = ing_item.get('qty', 0)
                    total_ing_qty_for_event_platillo = ing_qty_per_platillo * num_invitados
                    
                    current_total = required_map.get(ing_id, 0)
                    required_map[ing_id] = current_total + total_ing_qty_for_event_platillo
    
    results = []
    for ing_id, total_qty in required_map.items():
        ing_doc = db.ingredientes.find_one({'_id': ObjectId(ing_id)})
        if ing_doc:
            results.append({
                "ingrediente": Ingrediente(**ing_doc).json(),
                "total_qty_requerida": total_qty
            })
    return jsonify(results), 200 

# CRUD de ingredientes

@banquet_admin_bp.route('/ingredients', methods=['GET'])
def get_all_ingredients_admin():
    ingredients_cursor = db.ingredientes.find()
    ingredients_list = [Ingrediente(**i).json() for i in ingredients_cursor]
    return jsonify(ingredients_list), 200 

@banquet_admin_bp.route('/ingredients/<string:ingredient_id>', methods=['GET'])
def get_ingredient_by_id(ingredient_id):
    try:
        ing_obj_id = ObjectId(ingredient_id)
    except Exception:
        return jsonify({"mensaje": "ID de ingrediente inválido"}), 400
    
    ingredient_doc = db.ingredientes.find_one({'_id': ing_obj_id})
    if ingredient_doc:
        return jsonify(Ingrediente(**ingredient_doc).json()), 200 
    return jsonify({"mensaje": "Ingrediente no encontrado"}), 404

@banquet_admin_bp.route('/ingredients', methods=['POST'])
def create_ingredient():
    data = request.get_json()
    if not data or not data.get('descripcion') or not data.get('unidad'):
        return jsonify({"mensaje": "Campos 'descripcion' y 'unidad' requeridos"}), 400
    
    ing_data = {"descripcion": data['descripcion'], "unidad": data['unidad']}
    if db.ingredientes.find_one(ing_data): 
        return jsonify({"mensaje": "Ingrediente con esa descripción y unidad ya existe"}), 409
        
    new_ingredient = Ingrediente(**ing_data)
    try:
        inserted_id = new_ingredient.save()
        created_ing = db.ingredientes.find_one({'_id': inserted_id})
        return jsonify(Ingrediente(**created_ing).json()), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error al crear ingrediente: {e}"}), 500

@banquet_admin_bp.route('/ingredients/<string:ingredient_id>', methods=['PUT'])
@roles_required(allowed_roles=['admin_banquetes'])
def update_ingredient_admin(ingredient_id):
    data = request.get_json()
    try:
        ing_obj_id = ObjectId(ingredient_id)
    except Exception:
        return jsonify({"mensaje": "ID de ingrediente inválido"}), 400

    if not db.ingredientes.find_one({'_id': ing_obj_id}):
        return jsonify({"mensaje": "Ingrediente no encontrado"}), 404
    
    update_data = {}
    if 'descripcion' in data: update_data['descripcion'] = data['descripcion']
    if 'unidad' in data: update_data['unidad'] = data['unidad']
    if not update_data:
        return jsonify({"mensaje": "No hay datos para actualizar"}), 400

    result = db.ingredientes.update_one({'_id': ing_obj_id}, {'$set': update_data})
    if result.modified_count > 0:
        updated_ing = db.ingredientes.find_one({'_id': ing_obj_id})
        return jsonify(Ingrediente(**updated_ing).json()), 200
    return jsonify({"mensaje": "No se pudo actualizar o no hubo cambios"}), 304

@banquet_admin_bp.route('/ingredients/<string:ingredient_id>', methods=['DELETE'])
@roles_required(allowed_roles=['admin_banquetes'])
def delete_ingredient_admin(ingredient_id):
    try:
        ing_obj_id = ObjectId(ingredient_id)
    except Exception:
        return jsonify({"mensaje": "ID de ingrediente inválido"}), 400
    
    result = db.ingredientes.delete_one({'_id': ing_obj_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Ingrediente eliminado."}), 200
    return jsonify({"mensaje": "Ingrediente no encontrado."}), 404


# CRUD platillos

@banquet_admin_bp.route('/platillos', methods=['GET'])
def obtenerPlatillos():
    query = {}
    tipo_platillo_filter = request.args.get('tipo_platillo')
    if tipo_platillo_filter:
        query['tipo_platillo'] = tipo_platillo_filter

    platillos_cursor = db.platillos.find(query)
    platillos_list = [enrich_platillo(Platillo(**p).json()) for p in platillos_cursor]
    return jsonify(platillos_list), 200

@banquet_admin_bp.route('/platillos', methods=['POST'])
def crearPlatillo():
    data = request.get_json()
    req_fields = ['nombre', 'descripcion', 'tipo_platillo', 'precio', 'ingredientes']
    if not all(field in data for field in req_fields):
        return jsonify({"mensaje": "Faltan campos requeridos para el platillo"}), 400

    processed_ingredientes = []
    for ing_item in data.get('ingredientes', []):
        
        if not ing_item.get('ingrediente') or not isinstance(ing_item.get('qty'), (int, float)):
            return jsonify({"mensaje": "Formato de ingrediente inválido"}), 400
        try:
            ing_obj_id = ObjectId(ing_item['ingrediente'])
            if not db.ingredientes.find_one({'_id': ing_obj_id}):
                 return jsonify({"mensaje": f"Ingrediente ID {ing_item['ingrediente']} no encontrado"}), 404
            processed_ingredientes.append({"ingrediente": ing_obj_id, "qty": ing_item['qty']})
        except:
            return jsonify({"mensaje": f"ID de ingrediente inválido: {ing_item['ingrediente']}"}), 400


    platillo_data = {
        "nombre": data['nombre'],
        "descripcion": data['descripcion'],
        "tipo_platillo": data['tipo_platillo'],
        "precio": float(data['precio']),
        "thumbnail": data.get('thumbnail', ''),
        "ingredientes": processed_ingredientes 
    }
    new_platillo = Platillo(**platillo_data)
    try:
        inserted_id = new_platillo.save()
        created_platillo_doc = db.platillos.find_one({'_id': inserted_id})
        return jsonify(enrich_platillo(Platillo(**created_platillo_doc).json())), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error al crear platillo: {e}"}), 500

@banquet_admin_bp.route('/platillos/<string:platillo_id>', methods=['PUT'])
def actualizarPlatillo(platillo_id):
    data = request.get_json()
    try:
        p_obj_id = ObjectId(platillo_id)
    except:
        return jsonify({"mensaje": "ID de platillo inválido"}), 400

    if not db.platillos.find_one({'_id': p_obj_id}):
        return jsonify({"mensaje": "Platillo no encontrado"}), 404

    update_data = {}
    simple_fields = ['nombre', 'descripcion', 'tipo_platillo', 'precio', 'thumbnail']
    for f in simple_fields:
        if f in data: update_data[f] = data[f]
    if 'precio' in update_data: update_data['precio'] = float(update_data['precio'])

    if 'ingredientes' in data:
        processed_ingredientes = []
        for ing_item in data.get('ingredientes', []):
            if not ing_item.get('ingrediente') or not isinstance(ing_item.get('qty'), (int, float)):
                return jsonify({"mensaje": "Formato de ingrediente inválido en actualización"}), 400
            try:
                ing_obj_id = ObjectId(ing_item['ingrediente'])
                if not db.ingredientes.find_one({'_id': ing_obj_id}):
                    return jsonify({"mensaje": f"Ingrediente ID {ing_item['ingrediente']} no encontrado"}), 404
                processed_ingredientes.append({"ingrediente": ing_obj_id, "qty": ing_item['qty']})
            except:
                return jsonify({"mensaje": f"ID de ingrediente inválido: {ing_item['ingrediente']}"}), 400
        update_data['ingredientes'] = processed_ingredientes
    
    if not update_data:
        return jsonify({"mensaje": "No hay datos para actualizar"}), 400

    result = db.platillos.update_one({'_id': p_obj_id}, {'$set': update_data})
    if result.modified_count > 0:
        updated_p = db.platillos.find_one({'_id': p_obj_id})
        return jsonify(enrich_platillo(Platillo(**updated_p).json())), 200
    return jsonify({"mensaje": "No se pudo actualizar o no hubo cambios"}), 304

@banquet_admin_bp.route('/platillos/<string:platillo_id>', methods=['DELETE'])
def borrarPlatillo(platillo_id):
    try:
        p_obj_id = ObjectId(platillo_id)
    except:
        return jsonify({"mensaje": "ID de platillo inválido"}), 400
    
    result = db.platillos.delete_one({'_id': p_obj_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Platillo eliminado."}), 200
    return jsonify({"mensaje": "Platillo no encontrado."}), 404

#CRUD de salones

@banquet_admin_bp.route('/salons', methods=['GET'])
def obtenerSalones():
    salones_cursor = db.salones.find()
    salones_list = [Salon(**s).json() for s in salones_cursor]
    return jsonify(salones_list), 200

@banquet_admin_bp.route('/salons', methods=['POST'])
def agregarSalon():
    data = request.get_json()
    req_fields = ['nombre', 'descripcion', 'capacidad']
    if not all(field in data for field in req_fields):
        return jsonify({"mensaje": "Faltan campos requeridos para el salón"}), 400
    
    salon_data = {
        "nombre": data['nombre'],
        "descripcion": data['descripcion'],
        "capacidad": int(data['capacidad'])
    }
    new_salon = Salon(**salon_data)
    try:
        inserted_id = new_salon.save()
        created_salon = db.salones.find_one({'_id': inserted_id})
        return jsonify(Salon(**created_salon).json()), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error al crear salón: {e}"}), 500

@banquet_admin_bp.route('/salons/<string:salon_id>', methods=['PUT'])
def actualizarSalon(salon_id):
    data = request.get_json()
    try:
        s_obj_id = ObjectId(salon_id)
    except:
        return jsonify({"mensaje": "ID de salón inválido"}), 400
    
    if not db.salones.find_one({'_id': s_obj_id}):
        return jsonify({"mensaje": "Salón no encontrado"}), 404

    update_data = {}
    if 'nombre' in data: update_data['nombre'] = data['nombre']
    if 'descripcion' in data: update_data['descripcion'] = data['descripcion']
    if 'capacidad' in data: update_data['capacidad'] = int(data['capacidad'])
    if not update_data:
        return jsonify({"mensaje": "No hay datos para actualizar"}), 400

    result = db.salones.update_one({'_id': s_obj_id}, {'$set': update_data})
    if result.modified_count > 0:
        updated_s = db.salones.find_one({'_id': s_obj_id})
        return jsonify(Salon(**updated_s).json()), 200
    return jsonify({"mensaje": "No se pudo actualizar o no hubo cambios"}), 304

@banquet_admin_bp.route('/salons/<string:salon_id>', methods=['DELETE'])
def borrarSalon(salon_id):
    try:
        s_obj_id = ObjectId(salon_id)
    except:
        return jsonify({"mensaje": "ID de salón inválido"}), 400
    
    result = db.salones.delete_one({'_id': s_obj_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Salón eliminado."}), 200
    return jsonify({"mensaje": "Salón no encontrado."}), 404
