from flask import Flask

def register_blueprints(app: Flask):
    from .auth_routes import auth_bp
    from .public_routes import public_bp
    from .client_routes import clients_bp
    from .banquet_admin_routes import banquet_admin_bp
    from .salon_admin_routes import salon_admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(public_bp, url_prefix='/public')
    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(banquet_admin_bp, url_prefix='/banquet-admin')
    app.register_blueprint(salon_admin_bp, url_prefix='/salon-admin')