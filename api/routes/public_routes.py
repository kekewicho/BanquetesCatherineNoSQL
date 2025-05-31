from flask import Blueprint, jsonify, request
from models.Salon import Salon #
from models.Evento import Platillo, Ingrediente #
from config.conexion_mongo import db
from bson import ObjectId

public_bp = Blueprint('public_bp', __name__)

def enrich_platillo(platillo_doc):
    """Helper to enrich a platillo document with its ingredients."""
    if 'ingredientes' in platillo_doc and isinstance(platillo_doc['ingredientes'], list):
        enriched_ingredientes = []
        for item in platillo_doc['ingredientes']:
            ingrediente_id = item.get('ingrediente') # This is an ObjectId in the model
            qty = item.get('qty')
            if ingrediente_id:
                ing_obj_doc = db.ingredientes.find_one({'_id': ObjectId(ingrediente_id)})
                if ing_obj_doc:
                    enriched_ingredientes.append({
                        "ingrediente": Ingrediente(**ing_obj_doc).json(),
                        "qty": qty
                    })
        platillo_doc['ingredientes'] = enriched_ingredientes
    return platillo_doc

@public_bp.route('/salons', methods=['GET'])
def get_salons():
    salones_cursor = db.salones.find()
    salones_list = [Salon(**s).json() for s in salones_cursor]
    return jsonify(salones_list), 200 #

@public_bp.route('/salons/<string:salon_id>', methods=['GET'])
def get_salon_by_id(salon_id):
    try:
        salon_obj_id = ObjectId(salon_id)
    except Exception:
        return jsonify({"mensaje": "ID de salón inválido"}), 400
    
    salon_doc = db.salones.find_one({'_id': salon_obj_id})
    if salon_doc:
        return jsonify(Salon(**salon_doc).json()), 200 #
    return jsonify({"mensaje": "Salón no encontrado"}), 404

@public_bp.route('/platillos', methods=['GET'])
def get_platillos():
    query = {}
    tipo_platillo_filter = request.args.get('tipo_platillo')
    if tipo_platillo_filter:
        query['tipo_platillo'] = tipo_platillo_filter

    platillos_cursor = db.platillos.find(query)
    platillos_list = []
    for p_doc in platillos_cursor:
        platillo_obj = Platillo(**p_doc) # Create instance to use its .json() or manual enrichment
        # The .json() from Base doesn't do deep enrichment of 'ingredientes' list of dicts by default
        # Manual enrichment or enhanced Platillo.json() is needed
        enriched_p_doc = platillo_obj.json() # Base.json() will convert OID to str
        enriched_p_doc = enrich_platillo(enriched_p_doc) # Custom enrichment
        platillos_list.append(enriched_p_doc)
        
    return jsonify(platillos_list), 200 #

@public_bp.route('/platillos/<string:platillo_id>', methods=['GET'])
def get_platillo_by_id(platillo_id):
    try:
        platillo_obj_id = ObjectId(platillo_id)
    except Exception:
        return jsonify({"mensaje": "ID de platillo inválido"}), 400

    platillo_doc = db.platillos.find_one({'_id': platillo_obj_id})
    if platillo_doc:
        platillo_obj = Platillo(**platillo_doc)
        enriched_p_doc = platillo_obj.json()
        enriched_p_doc = enrich_platillo(enriched_p_doc)
        return jsonify(enriched_p_doc), 200 #
    return jsonify({"mensaje": "Platillo no encontrado"}), 404