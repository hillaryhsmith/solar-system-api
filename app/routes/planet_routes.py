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