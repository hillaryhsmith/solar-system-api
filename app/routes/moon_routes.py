from flask import Blueprint, jsonify, abort, make_response, request
from app.models.moon import Moon
from app import db

bp = Blueprint("moons_bp",__name__, url_prefix="/moons")


def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))
    
# POST /moons
@bp.route("", methods=["POST"])
def create_moon():
    request_body = request.get_json()

    try:
        moon = Moon.from_dict(request_body)
    except KeyError as error:
        error_message(f"Missing key: {error}", 400)

    db.session.add(moon)
    db.session.commit()

    return jsonify(moon.make_dict()), 201

# GET /moons
@bp.route("", methods=["GET"])
def list_moons():

    name_param = request.args.get("name")
    if name_param:
        moons = Moon.query.filter_by(name=name_param)

    list_of_moons = [moon.make_dict() for moon in moons]

    return jsonify(list_of_moons)