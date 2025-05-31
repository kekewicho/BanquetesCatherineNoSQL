from flask import Flask
from routes import register_blueprints
from controller.PlatilloController import platillo_bp
from controller.EventoController import evento_bp

app = Flask(__name__)
app.register_blueprint(usuario_bp)


if __name__ == "__main__":
    app.run(debug=True)