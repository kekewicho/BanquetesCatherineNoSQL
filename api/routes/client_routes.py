from flask import Blueprint, request, jsonify, session
from models.User import Cliente #
from models.Evento import Evento, Platillo, Ingrediente #
from models.Salon import Salon #
from config.conexion_mongo import db
from bson import ObjectId
from utils.decorators import login_required, roles_required
from datetime import datetime, timedelta

clients_bp = Blueprint('clients_bp', __name__)

def convert_objectids(obj):
    if isinstance(obj, dict):
        return {k: convert_objectids(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectids(i) for i in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

def enrich_event_details(event_doc_or_obj):
    if isinstance(event_doc_or_obj, Evento):
        event_data = event_doc_or_obj.json()
    else:
        event_data = event_doc_or_obj 
        if '_id' in event_data and isinstance(event_data['_id'], ObjectId):
            event_data['_id'] = str(event_data['_id'])

    if event_data.get('salon') and isinstance(event_data['salon'], (str, ObjectId)):
        salon_doc = db.salones.find_one({'_id': ObjectId(event_data['salon'])})
        event_data['salon'] = Salon(**salon_doc).json() if salon_doc else None

    if event_data.get('menu') and isinstance(event_data['menu'], list):
        enriched_menu = []
        for p_id_str in event_data['menu']:
            p_doc = db.platillos.find_one({'_id': ObjectId(p_id_str)})
            if p_doc:
                enriched_platillo_doc = Platillo(**p_doc).json()
                enriched_platillo_doc = enrich_platillo(enriched_platillo_doc)
                enriched_menu.append(enriched_platillo_doc)
        event_data['menu'] = enriched_menu
    
    if event_data.get('plantilla') and isinstance(event_data['plantilla'], list):
        enriched_plantilla = []
        for staff_id_str in event_data['plantilla']:
            staff_doc = db.usuarios.find_one({'_id': ObjectId(staff_id_str)})
            if staff_doc:
                enriched_plantilla.append({
                    "_id": str(staff_doc["_id"]),
                    "nombre": staff_doc["nombre"],
                    "role": staff_doc["role"]
                })
        event_data['plantilla'] = enriched_plantilla

    if event_data.get('cliente_id') and isinstance(event_data['cliente_id'], (str, ObjectId)):
        client_doc = db.usuarios.find_one({'_id': ObjectId(event_data['cliente_id']), 'role': 'cliente'})
        if client_doc:
            event_data['cliente'] = Cliente(**client_doc).json()

    return convert_objectids(event_data)


@clients_bp.route('/me', methods=['GET'])
@login_required
@roles_required(allowed_roles=['cliente']) # Ensure only clients access this
def get_my_profile():
    user_id = session['user'].get('id') # Assuming ID is stored as 'id' after login
    if not user_id:
         user_id = session['user'].get('_id') # Fallback if stored as _id

    client_doc = db.usuarios.find_one({'_id': ObjectId(user_id), 'role': 'cliente'})
    if client_doc:
        # The User model has apellido, telefono, rfc, direccion as None by default
        # Cliente model is used when role is 'cliente'
        client_obj = Cliente(**client_doc)
        return jsonify(client_obj.json()), 200 #
    return jsonify({"mensaje": "Cliente no encontrado"}), 404


@clients_bp.route('/me/events', methods=['GET'])
@login_required
@roles_required(allowed_roles=['cliente'])
def get_my_events():
    user_id = session['user'].get('id') or session['user'].get('_id')
    
    query = {'cliente_id': ObjectId(user_id)} # Assuming Evento model stores 'cliente_id'

    status_filter = request.args.get('status')
    current_date_str = datetime.now().strftime("%Y-%m-%d")

    if status_filter == "upcoming":
        query['fecha'] = {'$gte': current_date_str}
    elif status_filter == "past":
        query['fecha'] = {'$lt': current_date_str}
    
    # Sorting by date, newest first for past, oldest first for upcoming
    sort_order = -1 if status_filter == "past" else 1
    
    events_cursor = db.eventos.find(query).sort("fecha", sort_order)
    events_list = [enrich_event_details(e_doc) for e_doc in events_cursor]
    return jsonify(events_list), 200 #

@clients_bp.route('/me/events/<string:event_id>', methods=['GET'])
@login_required
@roles_required(allowed_roles=['cliente'])
def get_my_event_details(event_id):
    user_id = session['user'].get('id') or session['user'].get('_id')
    try:
        event_obj_id = ObjectId(event_id)
    except Exception:
        return jsonify({"mensaje": "ID de evento inválido"}), 400

    event_doc = db.eventos.find_one({'_id': event_obj_id, 'cliente_id': ObjectId(user_id)})
    if event_doc:
        return jsonify(enrich_event_details(event_doc)), 200
    return jsonify({"mensaje": "Evento no encontrado o no autorizado"}), 404

@clients_bp.route('/me/events/<string:event_id>', methods=['PUT'])
@login_required
@roles_required(allowed_roles=['cliente'])
def update_my_event_guests(event_id):
    user_id = session['user'].get('id') or session['user'].get('_id')
    data = request.get_json()

    if 'invitados' not in data:
        return jsonify({"mensaje": "Número de invitados requerido"}), 400
    
    try:
        new_invitados = int(data['invitados'])
        if new_invitados < 0: # Or some other validation
            raise ValueError("Número de invitados no puede ser negativo")
    except ValueError as e:
        return jsonify({"mensaje": f"Valor de invitados inválido: {e}"}), 400

    try:
        event_obj_id = ObjectId(event_id)
    except Exception:
        return jsonify({"mensaje": "ID de evento inválido"}), 400

    event_doc = db.eventos.find_one({'_id': event_obj_id, 'cliente_id': ObjectId(user_id)})
    if not event_doc:
        return jsonify({"mensaje": "Evento no encontrado o no autorizado"}), 404

    # Check 3-day rule before event (Section 3.1 Eventos detalles)
    event_date = datetime.strptime(event_doc['fecha'], "%Y-%m-%d")
    if event_date - timedelta(days=3) <= datetime.now():
        return jsonify({"mensaje": "No se puede modificar el número de invitados con menos de 3 días de anticipación."}), 403

    update_result = db.eventos.update_one(
        {'_id': event_obj_id},
        {'$set': {'invitados': new_invitados, 'validated': False}} # Per README: may set validated to false
    )

    if update_result.modified_count > 0:
        updated_event_doc = db.eventos.find_one({'_id': event_obj_id})
        # TODO: Trigger notification for administrators
        return jsonify(enrich_event_details(updated_event_doc)), 200 #
    
    # If no modification, could be same value or error
    return jsonify({"mensaje": "No se pudo actualizar el evento o no hubo cambios."}), 400