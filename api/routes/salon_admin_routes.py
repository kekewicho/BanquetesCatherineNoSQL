from flask import Blueprint, request, jsonify, session
from models.User import Gerente 
from models.Evento import Evento 
from config.conexion_mongo import db
from bson import ObjectId
from utils.decorators import login_required, roles_required
from datetime import datetime, timedelta

from routes.client_routes import enrich_event_details 

salon_admin_bp = Blueprint('salon_admin_bp', __name__)

@salon_admin_bp.route('/me/events', methods=['GET'])
@roles_required(allowed_roles=['admin_salon']) 
def get_salon_admin_events():
    user_info = session.get('user')
    user_id_from_session = user_info.get('id') or user_info.get('_id')

    
    gerente_doc = db.usuarios.find_one({'_id': ObjectId(user_id_from_session), 'role': 'admin_salon'})
    if not gerente_doc:
        return jsonify({"mensaje": "Administrador de salón no encontrado o rol incorrecto."}), 403
    
    
    salon_id_managed_by_gerente = gerente_doc.get('salon') 
    if not salon_id_managed_by_gerente:
        return jsonify({"mensaje": "Administrador no está asociado a ningún salón."}), 404

    try:
        
        salon_obj_id = ObjectId(salon_id_managed_by_gerente) 
    except Exception:
         return jsonify({"mensaje": "ID de salón asociado al gerente es inválido."}), 500

    query = {'salon': salon_obj_id} 

    from_date_str = request.args.get('from_date')
    to_date_str = request.args.get('to_date')
    
    
    if not from_date_str and not to_date_str:
        from_date_str = datetime.now().strftime("%Y-%m-%d")
        to_date_str = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")

    if from_date_str:
        query.setdefault('fecha', {})['$gte'] = from_date_str
    if to_date_str:
        query.setdefault('fecha', {})['$lte'] = to_date_str
    
    events_cursor = db.eventos.find(query).sort("fecha", 1) 
    events_list = [enrich_event_details(e_doc) for e_doc in events_cursor]
    return jsonify(events_list), 200

@salon_admin_bp.route('/me/events/<string:event_id>', methods=['GET'])
@roles_required(allowed_roles=['admin_salon'])
def get_salon_admin_event_details(event_id):
    user_info = session.get('user')
    user_id_from_session = user_info.get('id') or user_info.get('_id')

    gerente_doc = db.usuarios.find_one({'_id': ObjectId(user_id_from_session), 'role': 'admin_salon'})
    if not gerente_doc:
        return jsonify({"mensaje": "Administrador de salón no encontrado o rol incorrecto."}), 403
    
    salon_id_managed_by_gerente = gerente_doc.get('salon')
    if not salon_id_managed_by_gerente:
        return jsonify({"mensaje": "Administrador no está asociado a ningún salón."}), 404
    
    try:
        event_obj_id = ObjectId(event_id)
        salon_obj_id_managed = ObjectId(salon_id_managed_by_gerente)
    except Exception:
        return jsonify({"mensaje": "ID de evento o salón inválido"}), 400

    
    event_doc = db.eventos.find_one({'_id': event_obj_id, 'salon': salon_obj_id_managed})
    if event_doc:
        return jsonify(enrich_event_details(event_doc)), 200
    
    return jsonify({"mensaje": "Evento no encontrado o no pertenece al salón de este administrador."}), 404