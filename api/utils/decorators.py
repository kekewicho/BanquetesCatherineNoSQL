from functools import wraps
from flask import session, jsonify

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"mensaje": "Autenticación requerida", "exito": False}), 401
        return f(*args, **kwargs)
    return decorated_function

def roles_required(allowed_roles):
    if not isinstance(allowed_roles, list):
        allowed_roles = [allowed_roles]
    def decorator(f):
        @wraps(f)
        @login_required # Ensures user is logged in first
        def decorated_function(*args, **kwargs):
            user_role = session['user'].get('role')
            if user_role not in allowed_roles:
                return jsonify({"mensaje": "Acceso no autorizado para este rol", "exito": False}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator