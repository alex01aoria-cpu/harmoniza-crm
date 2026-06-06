from app.models.lead import Lead
from app.models.user import User
from app.services.auth_service import AuthService


def auth_headers(client, db_session) -> dict[str, str]:
    user = User(
        email="gestao@harmoniza.com",
        password_hash=AuthService.hash_password("12345678"),
        full_name="Gestão Harmoniza",
        role="admin",
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        json={"email": "gestao@harmoniza.com", "password": "12345678"},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def create_lead(client, db_session) -> tuple[int, dict[str, str]]:
    headers = auth_headers(client, db_session)
    response = client.post(
        "/leads",
        json={
            "nome": "Marina Souza",
            "telefone": "47922223333",
            "canal_principal": "WhatsApp",
            "procedimento_entrada": "Botox",
            "temperatura": "Morna",
            "qualificacao": "Em análise",
            "status_atual": "Lead nova",
            "responsavel_atual": "Hermes / Triagem",
        },
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()["id"], headers


def test_pipeline_transition_updates_status_and_records_history(client, db_session) -> None:
    lead_id, headers = create_lead(client, db_session)

    response = client.patch(
        f"/leads/{lead_id}/stage",
        json={
            "novo_status": "Qualificada",
            "responsavel_atual": "Vendedora",
            "observacao": "Lead confirmou interesse e orçamento aproximado.",
        },
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["lead"]["status_atual"] == "Qualificada"
    assert body["lead"]["responsavel_atual"] == "Vendedora"
    assert body["history"]["status_origem"] == "Lead nova"
    assert body["history"]["status_destino"] == "Qualificada"
    assert body["history"]["alterado_por"] == "gestao@harmoniza.com"

    from app.models.pipeline_stage_history import PipelineStageHistory

    saved_lead = db_session.query(Lead).filter(Lead.id == lead_id).first()
    saved_history = (
        db_session.query(PipelineStageHistory)
        .filter(PipelineStageHistory.lead_id == lead_id)
        .first()
    )

    assert saved_lead is not None
    assert saved_lead.status_atual == "Qualificada"
    assert saved_lead.responsavel_atual == "Vendedora"
    assert saved_history is not None
    assert saved_history.status_origem == "Lead nova"
    assert saved_history.status_destino == "Qualificada"


def test_pipeline_transition_rejects_unknown_status(client, db_session) -> None:
    lead_id, headers = create_lead(client, db_session)

    response = client.patch(
        f"/leads/{lead_id}/stage",
        json={"novo_status": "Status inventado"},
        headers=headers,
    )

    assert response.status_code == 422
