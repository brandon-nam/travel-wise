def test_hello(client):
    response = client.get("/")
    assert response.status_code is not None
