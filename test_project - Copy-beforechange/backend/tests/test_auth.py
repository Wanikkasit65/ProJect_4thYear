def test_register_and_login(client):
    register_response = client.post(
        "/api/auth/register",
        json={
            "first_name": "Nina",
            "last_name": "Miles",
            "username": "nina",
            "email": "nina@example.com",
            "password": "password123",
        },
    )
    assert register_response.status_code == 201
    assert register_response.json()["username"] == "nina"

    login_response = client.post(
        "/api/auth/login",
        json={"username_or_email": "nina", "password": "password123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

