from fastapi.testclient import TestClient

from scripts.fastapi_demo import app

client = TestClient(app)


def test_root_handler():
    # Arrange
    expected = "version"

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert expected in body
    assert isinstance(body[expected], str)


def test_set_and_get_item():
    # Arrange
    key, value = "foo", "bar"

    # Act
    set_resp = client.get(f"/set/{key}/{value}")
    get_resp = client.get(f"/get/{key}")

    # Assert
    assert set_resp.status_code == 200
    assert get_resp.status_code == 200
    assert get_resp.json() == {"key": key, "value": value}


def test_set_and_get_compressed_item():
    # Arrange
    key, value = "cfoo", "cbar"

    # Act
    client.get(f"/set_compressed/{key}/{value}")
    resp = client.get(f"/get_compressed/{key}")

    # Assert
    assert resp.status_code == 200
    assert resp.json() == {"key": key, "value": value}


def test_set_and_get_binary_item():
    # Arrange
    key, value = "bfoo", "bbar"

    # Act
    client.get(f"/set_binary/{key}/{value}")
    resp = client.get(f"/get_binary/{key}")

    # Assert
    assert resp.status_code == 200
    assert resp.json()["value"] == value


def test_set_and_get_binary_compressed_item():
    # Arrange
    key, value = "bcfoo", "bcbar"

    # Act
    client.get(f"/set_binary_compressed/{key}/{value}")
    resp = client.get(f"/get_binary_compressed/{key}")

    # Assert
    assert resp.status_code == 200
    assert resp.json()["value"] == value


def test_size_handler():
    # Arrange
    client.get("/set/foo/bar")
    client.get("/set/baz/qux")

    # Act
    resp = client.get("/size")

    # Assert
    assert resp.status_code == 200
    body = resp.json()
    assert "size" in body
    assert isinstance(body["size"], (int, type(None)))
