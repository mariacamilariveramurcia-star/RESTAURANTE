from flask import Flask
from models import db, seed_data

# Importamos los tres Blueprints
from paginas.rutas import paginas_bp
from admin.rutas   import admin_bp
from api.rutas     import api_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'camcam-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurante.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos la base de datos con la app
db.init_app(app)

# Registramos los tres Blueprints en la aplicación principal
app.register_blueprint(paginas_bp)           # rutas: /  /menu  /dish/<id>  /pedidos
app.register_blueprint(admin_bp)             # rutas: /admin/
app.register_blueprint(api_bp)               # rutas: /api/...

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True, port=5000)
