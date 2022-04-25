from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)

    from .routes import planet_routes
    app.register_blueprint(planet_routes.bp)

    return app
