# App.ipynb (celda 1)
from flask import Flask
from controller.UsuarioController import usuario_bp

app = Flask(__name__)
app.register_blueprint(usuario_bp)

print(app.url_map)

if __name__ == "__main__":
    app.run()