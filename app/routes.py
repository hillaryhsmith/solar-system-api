from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, has_moon=None):
        self.id = id
        self.name = name
        self.description = description
        self.has_moon = has_moon

planets = [
    Planet(1, "Mercury", "terrestrial", False),
    Planet(2, "Jupiter", "gaseous", True),
    Planet(3, "Earth", "terrestrial", True)
]

bp = Blueprint("planets_bp",__name__, url_prefix="/planets")

@bp.route("", methods=["GET"])
def list_planets():
    list_of_planets = [dict(
        id = planet.id,
        name = planet.name,
        description = planet.description,
        has_moon = planet.has_moon,  
    ) for planet in planets]

    return jsonify(list_of_planets)

@bp.route("/<id>", methods=["GET"])
def get_planet(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({"message":f"planet {id} invalid"}), 400
    
    for planet in planets:
        if planet.id == id:
            return jsonify(dict(
                id = planet.id,
                name = planet.name,
                description = planet.description,
                has_moon = planet.has_moon))
    return jsonify({"message":f"planet {id} not found"}), 404
