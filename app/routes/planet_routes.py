from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planet import Planet
from app import db

bp = Blueprint("planets_bp",__name__, url_prefix="/planets")

# helper functions
def get_planet_record_by_id(id):
    try: 
        id = int(id)
    except ValueError:
        error_message(f"Invalid planet id {id}", 400)
    
    planet = Planet.query.get(id)

    if planet:
        return planet
    
    error_message(f"No planet with id {id} found", 404)
    
def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

# POST /planets
@bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()

    try:
        planet = Planet.from_dict(request_body)
    except KeyError as error:
        error_message(f"Missing key: {error}", 400)

    db.session.add(planet)
    db.session.commit()

    return jsonify(planet.make_dict()), 201

# GET /planets
@bp.route("", methods=["GET"])
def list_planets():
    description_param = request.args.get("description")
    name_param = request.args.get("name")
    has_moon_param = request.args.get("has_moon")

    if description_param:
        planets = Planet.query.filter_by(description=description_param)
    elif name_param:
        planets = Planet.query.filter_by(name=name_param)
    elif has_moon_param:
        planets = Planet.query.filter_by(has_moon=has_moon_param)
    else:
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

    try: 
        planet.replace_all_details(request_body)
    except KeyError as error:
        error_message(f"Missing key: {error}", 400)

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
    planet.replace_some_details(request_body)

    db.session.commit()
    
    return jsonify(planet.make_dict())