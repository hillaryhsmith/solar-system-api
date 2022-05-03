import re
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planet import Planet
from app import db

# class Planet:
#     def __init__(self, id, name, description, has_moon=None):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.has_moon = has_moon

#     def make_dict(self):
#         return dict(
#                 id = self.id,
#                 name = self.name,
#                 description = self.description,
#                 has_moon = self.has_moon,  
#             )

# planets = [
#     Planet(1, "Mercury", description="terrestrial", has_moon=False),
#     Planet(2, "Jupiter", description="gaseous", has_moon=True),
#     Planet(3, "Earth", description="terrestrial", has_moon=True)
# ]

bp = Blueprint("planets_bp",__name__, url_prefix="/planets")

# POST /planets
@bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    planet = Planet(
        name = request_body["name"], 
        description = request_body["description"],
        has_moon = request_body["has_moon"]
        )
    db.session.add(planet)
    db.session.commit()

    return jsonify(planet.make_dict()), 201

# GET /planets
@bp.route("", methods=["GET"])
def list_planets():
    planets = Planet.query.all()
    list_of_planets = [planet.make_dict() for planet in planets]

    return jsonify(list_of_planets)


# GET /planets/<planet_id>

@bp.route("/<planet_id>", methods=["GET"])
def get_planet_by_id(planet_id):
    planet = get_planet_record_by_id(planet_id)
    return jsonify(planet.make_dict())

# PUT /planets/<planet_id>
@bp.route("/<planet_id>", methods=["PUT"])
def replace_planet_by_id(planet_id):
    request_body = request.get_json()
    planet = get_planet_record_by_id(planet_id)
    
    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.has_moon = request_body["has_moon"]
    
    db.session.commit()

    return jsonify(planet.make_dict())

# DELETE /planets/<planet_id>
@bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet_by_id(planet_id):
    planet = get_planet_record_by_id(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"Planet with id {planet_id} successfully deleted")

# PATCH /planets/<planet_id>
@bp.route("/<planet_id>", methods=["PATCH"])
def update_planet_by_id(planet_id):
    request_body = request.get_json()
    planet = get_planet_record_by_id(planet_id)
    planet_keys = request_body.keys()
    
    if "name" in planet_keys: 
        planet.name = request_body["name"]
    if "description" in planet_keys: 
        planet.description = request_body["description"]
    if "has_moon" in planet_keys: 
        planet.has_moon = request_body["has_moon"]

    db.session.commit()
    return jsonify(planet.make_dict())

# helper function
def get_planet_record_by_id(id):
    try: 
        id = int(id)
    except ValueError:
        abort(make_response(jsonify(dict(details=f"Invalid planet id {id}")), 400))
    
    planet = Planet.query.get(id)

    if planet:
        return planet
    
    abort(make_response(jsonify(dict(details=f"No planet with id {id} found")), 404))




# def validate_planet(id):
#     try:
#         id = int(id)
#     except ValueError:
#         abort(make_response(jsonify(dict(message=f"planet {id} is invalid")), 400))

#     for planet in planets:
#         if planet.id == id:
#             return planet

#     abort(make_response(jsonify(dict(message=f"planet {id} not found")), 404))

# # GET planets/id
# @bp.route("/<id>", methods=["GET"])
# def get_planet(id):
#     planet = validate_planet(id)
#     return jsonify(planet.make_dict())