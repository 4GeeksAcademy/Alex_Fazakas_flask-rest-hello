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
