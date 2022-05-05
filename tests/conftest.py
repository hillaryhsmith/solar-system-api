import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.planet import Planet


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_planets(app):
    tatooine = Planet(id=1, name="Tatooine", description="desert", has_moon=True)
    hoth = Planet(id=2, name="Hoth", description="icy tundra", has_moon=True)

    db.session.add(tatooine)
    db.session.add(hoth)
    db.session.commit()