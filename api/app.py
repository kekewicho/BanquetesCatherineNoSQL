# App.ipynb (celda 1)
from flask import Flask
from controller.UsuarioController import usuario_bp
from controller.PlatilloController import platillo_bp
from controller.EventoController import evento_bp

app = Flask(__name__)

app.register_blueprint(usuario_bp)
app.register_blueprint(platillo_bp)
app.register_blueprint(evento_bp)

print(app.url_map)

if __name__ == "__main__":
    app.run()