import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from utils import APIException, generate_sitemap
from models import db, User, Character, Planet, Favorito

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Character, db.session))

app = Flask(__name__)
app.url_map.strict_slashes = False
db_url = os.getenv("DATABASE_URL")

if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/character', methods=['GET'])
def get_character():
    all_character = Character.query.all()
    results = [character.serialize() for character in all_character]
    return jsonify(results), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_id(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify(), 404
    return jsonify(character.serialize()), 200

@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.email)).scalars()
    result = [user.serialize()for user in users]
    response_body = {
        "mensaje": "estos sin tus usuarios",
        "result": result
    }
    return response_body, 200

# Ruta para listar todos los favoritos del usuario actual
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # Aquí debes obtener el usuario actual, por ejemplo, utilizando la información del token de autenticación si estás utilizando autenticación.
    # Por ahora, supondrémos que tienes el usuario en una variable llamada "current_user".
    user_favorites = Favorito.query.filter_by(user_id=current_user.id).all()
    favorites_list = [favorite.serialize() for favorite in user_favorites]
    return jsonify(favorites_list), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(planet_id):
    # Aquí debes obtener el usuario actual de manera similar a la función anterior.
    # Luego, creas un nuevo favorito asociado al usuario con el planeta especificado.
    new_favorite = Favorito(user_id=current_user.id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Nuevo favorito de planeta añadido"}), 201    

# Ruta para añadir un nuevo personaje favorito al usuario actual
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_favorite(people_id):
    # Similar a la función anterior, pero esta vez asociando el ID del personaje en lugar del planeta.
    new_favorite = Favorito(user_id=current_user.id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Nuevo favorito de personaje añadido"}), 201  


# Ruta para eliminar un planeta favorito del usuario actual
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    # Similar a las funciones anteriores, pero en lugar de añadir un favorito, aquí eliminas uno existente.
    favorito = Favorito.query.filter_by(user_id=current_user.id, planet_id=planet_id).first()
    if favorito:
        db.session.delete(favorito)
        db.session.commit()
        return jsonify({"message": "Favorito de planeta eliminado"}), 200
    else:
        return jsonify({"message": "Favorito de planeta no encontrado"}), 404 

# Ruta para eliminar un personaje favorito del usuario actual
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite(people_id):
    # Similar a la función anterior, pero para favoritos de personajes.
    favorito = Favorito.query.filter_by(user_id=current_user.id, people_id=people_id).first()
    if favorito:
        db.session.delete(favorito)
        db.session.commit()
        return jsonify({"message": "Favorito de personaje eliminado"}), 200
    else:
        return jsonify({"message": "Favorito de personaje no encontrado"}), 404             





"""    
@app.route('/users/<int:users_id>', methods=['GET'])
def get_users_id(users_id):
    user = user.query.get(users_id)
    if user is None:
        return jsonify(), 404
    return jsonify(user.serialize()), 200 """

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
