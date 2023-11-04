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
from models import db, User, People, Planet, Favorite
#from models import Person
# import requests

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#get people = characters
@app.route("/people", methods=["GET"])
def get_people():
    people = People.query.all()
    people = list(map(lambda item: item.serialize(), people))
    return jsonify(people), 200

#get people by id
@app.route("/people/<int:theid>", methods=["GET"])
def get_one_person(theid = None):
    if theid is None:
        return jsonify({"message":"please specify the id"}), 400
    else:
        people = People.query.get(theid)
    
    if people is None:
        return jsonify({"message":"user not found"}), 404
    else:
        people = people.serialize()
        return jsonify(people), 200

#getPlanet
@app.route("/planet", methods=["GET"])
def get_planet():
    planet = Planet.query.all()
    planet = list(map(lambda item: item.serialize(), planet))
    return jsonify(planet), 200

#getOnePlanet
@app.route("/planet/<int:theid>", methods =["GET"])
def get_one_planet(theid):
    planet = Planet.query.get(theid)
    if planet is None:
        return jsonify({"message":"planet doesnt exist"})
    else:
        planet = planet.serialize()
        return jsonify(planet)
    
#getUsers
@app.route('/users', methods=['GET'])
def get_user():
    user = User.query.all()
    user = list(map(lambda item: item.serialize(), user))
    return 

#addFavoritePlanet or Character
@app.route("/favorite/<string:nature>/<int:nature_id>/<int:user_id>", methods=["POST"])
def add_favorite(nature, nature_id, user_id):
    if nature.lower() == "planet":
        favorite = Favorite.query.filter_by(user_id = user_id, planet_id = nature_id).first()
        if favorite is not None:
            return jsonify({"message":"planet exists in favorite"}), 400
        
        planet = Favorite(user_id = user_id, planet_id=nature_id)
        
        try:
            db.session.add(planet)
            db.session.commit()
            return jsonify({"message":"added succesfully"}), 201
        except Exception as error:
            print(error)
            db.session.rollback()
            return jsonify({"message":"error adding planet"}), 500
        
    if nature.lower() == "people":
        favorite = Favorite.query.filter_by(user_id = user_id, people_id = nature_id).first()
        if favorite is not None:
            return jsonify({"message":"character exists in favorite"}), 400
        people = Favorite(user_id = user_id, people_id=nature_id)
        
        try:
            db.session.add(people)
            db.session.commit()
            return jsonify({"message":"added succesfully"}), 201
        except Exception as error:
            print(error)
            db.session.rollback()
            return jsonify({"message":"error adding a character"}), 500

#deletePlanetOrCharacter
@app.route("/<string:nature>/<int:id_nature>", methods=["DELETE"])
def delete_planet_or_people(nature, id_nature):
    if nature.lower() == "people":
        people = People.query.get(id_nature)
        if people is None:
            return jsonify({"message":"there is no character to delete"}), 404
        else:
            try:
                db.session.delete(people)
                db.session.commit()
                return jsonify({"message":"character deleted"}), 200
            except Exception as error:
                print(error)
                db.session.rollback()
                return jsonify({"message":"error adding a character"}), 501
    
    if nature.lower() == "planet":
        planet = Planet.query.get(id_nature)
        if planet is None:
            return jsonify({"message":"there is no planet to delete"}), 404
        else:
            try:
                 db.session.delete(planet)
                 db.session.commit()
                 return jsonify({"message":"planet deleted"}), 200
            except Exception as error:
                print(error)
                db.session.rollback()
                return jsonify({"message":"error adding a planet"}), 501
            

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
