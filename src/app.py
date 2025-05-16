"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, People, Planets, Favorites
from sqlalchemy import select
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# USERS


@app.route("/users", methods=["GET"])
def get_all_users():
    stmt = select(Users)
    # como es todos devuelve una colección de los registros
    users = db.session.execute(stmt).scalars().all()
    # se pone el serialize xq es una lista?? es lista xq son todos los usuarios? hacer for in en los qe nos devuelve todos
    return jsonify([user.serialize()for user in users]), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    stmt = select(Users).where(Users.id == user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data or "name" not in data or "lastname" not in data:
        return jsonify({"error": "Missing data to create new user"}), 400

    new_user = Users(  # aqui ponemos los que tienen nullable=False ???
        email=data["email"],
        password=data["password"],
        name=data["name"],
        lastname=data["lastname"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201


@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    stmt = select(Users).where(Users.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "user not found"}), 404
    user.email = data.get("email", user.email)
    user.password = data.get("password", user.password)
    user.name = data.get("name", user.name)
    user.lastname = data.get("lastname", user.lastname)
    db.session.commit()
    return jsonify(user.serialize()), 200


@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    stmt = select(Users).where(Users.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "user not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "user deleted"}), 200

# PEOPLE


@app.route("/people", methods=["GET"])
def get_all_characters():
    stmt = select(People)
    characters = db.session.execute(stmt).scalars().all()
    return jsonify([character.serialize()for character in characters]), 200


@app.route("/people/<int:character_id>", methods=["GET"])
def get_one_character(character_id):
    stmt = select(People).where(People.id == character_id)
    character = db.session.execute(stmt).scalar_one_or_none()
    if character is None:
        return jsonify({"Error": "Character not found"}), 404
    return jsonify(character.serialize()), 200



@app.route("/people", methods=["POST"]) # da error que se va si añado nullable=True al model
def create_character():
    data = request.get_json()
    if not data or "character_name" not in data or "birth_year" not in data or "gender" not in data or "hair_color" not in data or "height" not in data or "films" not in data or "vehicles" not in data:
        return jsonify({"Error": "Missing data to create a new character"}), 400

    new_character = People(
        character_name=data["character_name"],
        birth_year=data["birth_year"],
        gender=data["gender"],
        hair_color=data["hair_color"],
        height=data["height"],
        films=data["films"],
        vehicles=data["vehicles"]
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201


@app.route("/people/<int:id>", methods=["PUT"])
def update_character(id):
    data = request.get_json()
    stmt = select(People).where(People.id == id)
    character = db.session.execute(stmt).scalar_one_or_none()
    if character is None:
        return jsonify({"error": "character not found"}), 404
    character.character_name = data.get(
        "character_name", character.character_name)
    character.birth_year = data.get("birth_year", character.birth_year)
    character.gender = data.get("gender", character.gender)
    character.hair_color = data.get("hair_color", character.hair_color)
    character.height = data.get("height", character.height)
    character.films = data.get("films", character.films)
    character.vehicles = data.get("vehicles", character.vehicles)
    db.session.commit()
    return jsonify(character.serialize()), 200


@app.route("/people/<int:id>", methods=["DELETE"])  # da error al eliminar data añadida con el seed.py
def delete_character(id):
    stmt = select(People).where(People.id == id)
    character = db.session.execute(stmt).scalar_one_or_none()
    if character is None:
        return jsonify({"Error": "Character not found"}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": "character deteled"}), 200

# PLANETS


@app.route("/planets", methods=["GET"])
def get_all_planets():
    stmt = select(Planets)
    planets = db.session.execute(stmt).scalars().all()
    return jsonify([planet.serialize()for planet in planets]), 200


@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    stmt = select(Planets).where(Planets.id == planet_id)
    planet = db.session.execute(stmt).scalar_one_or_none()
    if planet is None:
        return jsonify({"Error": "planet not found"}), 404
    return jsonify(planet.serialize()), 200


@app.route("/planets", methods=["POST"])
def create_planet():
    data = request.get_json()
    if not data or "planet_name" not in data or "population" not in data or "climate" not in data or "diameter" not in data or "gravity" not in data or "films" not in data:
        return jsonify({"error": "Missing data to create new planet"}), 400

    new_planet = Planets(
        planet_name=data["planet_name"],
        population=data["population"],
        climate=data["climate"],
        diameter=data["diameter"],
        gravity=data["gravity"],
        films=data["films"]
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201


@app.route("/planets/<int:id>", methods=["DELETE"])  # da error 500 al eliminar data añadida con el seed.py
def delete_planet(id):
    stmt = select(Planets).where(Planets.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"Error": "Planet not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"Message": "Planet deleted"}), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
