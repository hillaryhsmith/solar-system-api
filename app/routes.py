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

#instantiate blueprint object
bp = Blueprint("planets_bp",__name__, url_prefix="/planets")

#design endpoint with blueprint tag
"""..to get all existing planets, so that I can see a list of planets,
with their id, name, description, and other data of the planet."""

@bp.route("", methods=["GET"])
def list_planets():
    list_of_planets = [dict(
        id = planet.id,
        name = planet.name,
        description = planet.description,
        has_moon = planet.has_moon,  
    ) for planet in planets]

    return jsonify(list_of_planets)

# FLASK_ENV=developer flask run

    
