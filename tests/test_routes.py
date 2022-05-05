# Test GET /planets
def test_get_all_planets_with_empty_db_return_empty_list(client):
    response = client.get('/planets')

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

# Test GET /planets
def test_get_all_planets_using_fixture(client, two_planets):
    response = client.get('/planets')

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [{
        "id": 1,
        "name": "Tatooine",
        "description": "desert",
        "has_moon": True},
        {"id": 2,
        "name": "Hoth",
        "description": "icy tundra",
        "has_moon": True
    }]

# Test GET /planets/<id>
def test_get_one_planet_using_fixture(client, two_planets):
    response = client.get("/planets/1")

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Tatooine",
        "description": "desert",
        "has_moon": True
    } 

# Test GET /planets/<id>
def test_get_one_planet_no_db_data_return_404(client):
    response = client.get("/planets/1")

    assert response.status_code == 404

# Test POST /planets
def test_post_one_planet(client):
    response = client.post("/planets", json={
        "name": "Endor",
        "description": "Blue gas giant",
        "has_moon": True
    })

    response_body=response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Endor",
        "description": "Blue gas giant",
        "has_moon": True
    }