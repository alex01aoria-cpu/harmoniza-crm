from app.models.user import User
from app.services.auth_service import AuthService


def auth_headers(client, db_session) -> dict[str, str]:
    user = User(
        email="admin@harmoniza.com",
        password_hash=AuthService.hash_password("12345678"),
        full_name="Admin Harmoniza",
        role="admin",
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        json={"email": "admin@harmoniza.com", "password": "12345678"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_manual_lead_with_source(client, db_session) -> None:
    payload = {
        "nome": "Carla Mendes",
        "telefone": "47999998888",
        "canal_principal": "WhatsApp",
        "procedimento_entrada": "Botox",
        "objetivo_principal": "Suavizar marcas de expressão",
        "interesse_principal": "Botox",
        "duvida_principal": "Valor e disponibilidade",
        "conhece_clinica": False,
        "conhece_procedimento": True,
        "ja_fez_estetica": True,
        "historico_estetico_curto": "Já fez botox há mais de um ano",
        "temperatura": "Quente",
        "qualificacao": "Em análise",
        "status_atual": "Lead nova",
        "responsavel_atual": "Hermes / Triagem",
        "resumo_atual": "Lead manual cadastrada pela equipe",
        "proxima_acao": "Enviar primeira mensagem",
        "source": {
            "canal": "Meta Ads",
            "origem": "Formulário manual",
            "campanha": "Campanha Botox Junho",
            "conjunto": "Mulheres 30-45 Joinville",
            "anuncio": "Criativo antes e depois 01",
            "utm_source": "meta",
            "utm_medium": "paid_social",
            "utm_campaign": "botox_junho",
            "utm_content": "antes_depois_01",
            "utm_term": "botox",
            "landing_origem": "whatsapp-manual",
        },
    }

    response = client.post(
        "/leads",
        json=payload,
        headers=auth_headers(client, db_session),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] is not None
    assert body["nome"] == "Carla Mendes"
    assert body["status_atual"] == "Lead nova"
    assert body["source"]["campanha"] == "Campanha Botox Junho"
    assert body["source"]["utm_campaign"] == "botox_junho"


def test_list_leads_returns_recent_items_with_filters(client, db_session) -> None:
    headers = auth_headers(client, db_session)
    first_payload = {
        "nome": "Carla Mendes",
        "telefone": "47999998888",
        "canal_principal": "WhatsApp",
        "procedimento_entrada": "Botox",
        "temperatura": "Quente",
        "qualificacao": "Em análise",
        "status_atual": "Lead nova",
        "responsavel_atual": "Hermes / Triagem",
        "source": {
            "canal": "Meta Ads",
            "campanha": "Campanha Botox Junho",
            "utm_campaign": "botox_junho",
        },
    }
    second_payload = {
        **first_payload,
        "nome": "Julia Santos",
        "telefone": "47933334444",
        "status_atual": "Qualificada",
        "source": {
            "canal": "Meta Ads",
            "campanha": "Camp Skinbooster 8",
            "utm_campaign": "skinbooster_8",
        },
    }
    client.post("/leads", json=first_payload, headers=headers)
    client.post("/leads", json=second_payload, headers=headers)

    response = client.get(
        "/leads",
        params={"status_atual": "Lead nova", "campanha": "Campanha Botox Junho"},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["nome"] == "Carla Mendes"
    assert body[0]["status_atual"] == "Lead nova"
    assert body[0]["source"]["campanha"] == "Campanha Botox Junho"


def test_create_manual_lead_requires_authentication(client) -> None:
    response = client.post(
        "/leads",
        json={
            "nome": "Sem Auth",
            "telefone": "47911112222",
            "canal_principal": "WhatsApp",
            "procedimento_entrada": "Botox",
            "temperatura": "Fria",
            "qualificacao": "Em análise",
            "status_atual": "Lead nova",
            "responsavel_atual": "Hermes / Triagem",
        },
    )

    assert response.status_code == 401
