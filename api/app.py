from flask import Flask
from routes import register_blueprints

app = Flask(__name__)

app.secret_key = 'LabBaseDatos2'

register_blueprints(app)

if __name__ == "__main__":
    app.run(debug=True)