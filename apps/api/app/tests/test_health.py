from app.services.auth_service import AuthService


def test_healthcheck(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app": "Harmoniza CRM API",
        "environment": "development",
    }


def test_auth_login_and_me(client, db_session) -> None:
    from app.models.user import User

    user = User(
        email="admin@harmoniza.com",
        password_hash=AuthService.hash_password("12345678"),
        full_name="Admin Harmoniza",
        role="admin",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    login_response = client.post(
        "/auth/login",
        json={"email": "admin@harmoniza.com", "password": "12345678"},
    )

    assert login_response.status_code == 200
    payload = login_response.json()
    assert payload["token_type"] == "bearer"
    assert payload["user"]["email"] == "admin@harmoniza.com"

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {payload['access_token']}"},
    )

    assert me_response.status_code == 200
    assert me_response.json()["email"] == "admin@harmoniza.com"
