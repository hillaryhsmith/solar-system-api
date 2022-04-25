from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, has_moon=None):
        self.id = id
        self.name = name
        self.description = description
        self.has_moon = has_moon

    def make_dict(self):
        return dict(
                id = self.id,
                name = self.name,
                description = self.description,
                has_moon = self.has_moon,  
            )

planets = [
    Planet(1, "Mercury", "terrestrial", False),
    Planet(2, "Jupiter", "gaseous", True),
    Planet(3, "Earth", "terrestrial", True)
]

bp = Blueprint("planets_bp",__name__, url_prefix="/planets")

# GET /planets
@bp.route("", methods=["GET"])
def list_planets():
    list_of_planets = [planet.make_dict() for planet in planets]

    return jsonify(list_of_planets)

# GET planets/id
@bp.route("/<id>", methods=["GET"])
def get_planet(id):
    id = int(id)
    for planet in planets:
        if planet.id == id:
            return jsonify(planet.make_dict())
    # try:
    #     id = int(id)
    # except ValueError:
    #     return jsonify({"message":f"planet {id} invalid"}), 400

    # return jsonify({"message":f"planet {id} not found"}), 404
