from datetime import UTC, datetime, timedelta
from decimal import Decimal
from app.models.user import User
from app.services.auth_service import AuthService


def headers(client, db_session):
    user = User(email="ops@harmoniza.com", password_hash=AuthService.hash_password("12345678"), full_name="Ops", role="admin")
    db_session.add(user); db_session.commit()
    response = client.post("/auth/login", json={"email": "ops@harmoniza.com", "password": "12345678"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def create_lead(client, h, name="Lead Operacional"):
    response = client.post("/leads", json={
        "nome": name, "telefone": "47955554444", "canal_principal": "WhatsApp", "procedimento_entrada": "Botox",
        "temperatura": "Morna", "qualificacao": "Em análise", "status_atual": "Lead nova", "responsavel_atual": "Hermes / Triagem",
        "source": {"canal": "Meta Ads", "campanha": "Campanha Teste"}
    }, headers=h)
    assert response.status_code == 201
    return response.json()["id"]


def test_triage_handoff_tasks_outcomes_dashboard_and_ops(client, db_session):
    h = headers(client, db_session)
    lead_id = create_lead(client, h)

    triage = client.patch(f"/leads/{lead_id}/triage", json={
        "objetivo_principal": "Melhorar expressão", "interesse_principal": "Botox", "duvida_principal": "Preço",
        "conhece_clinica": True, "conhece_procedimento": True, "ja_fez_estetica": False,
        "temperatura": "Quente", "qualificacao": "Qualificada", "proxima_acao": "Enviar para vendedora"
    }, headers=h)
    assert triage.status_code == 200
    assert triage.json()["qualificacao"] == "Qualificada"

    handoff = client.post(f"/leads/{lead_id}/handoff", json={
        "responsavel_atual": "Vendedora", "resumo_atual": "Lead qualificada e pronta", "proxima_acao": "Agendar avaliação"
    }, headers=h)
    assert handoff.status_code == 200
    assert handoff.json()["lead"]["status_atual"] == "Passada para vendedora"

    task = client.post("/tasks", json={
        "lead_id": lead_id, "titulo": "Follow-up inicial", "responsavel": "Vendedora",
        "data_limite": (datetime.now(UTC) - timedelta(days=1)).isoformat(), "prioridade": "Alta"
    }, headers=h)
    assert task.status_code == 201

    overdue = client.get("/tasks", params={"overdue": True}, headers=h)
    assert overdue.status_code == 200
    assert len(overdue.json()) == 1

    outcome = client.put(f"/leads/{lead_id}/outcome", json={
        "agendou": True, "compareceu": True, "comprou": True, "valor_venda": "1200.00", "observacao_resultado": "Compra fechada"
    }, headers=h)
    assert outcome.status_code == 200
    assert Decimal(outcome.json()["valor_venda"]) == Decimal("1200.00")

    dashboard = client.get("/dashboard/summary", headers=h)
    assert dashboard.status_code == 200
    body = dashboard.json()
    assert body["leads_total"] >= 1
    assert body["compras"] == 1
    assert Decimal(body["ticket_medio"]) == Decimal("1200.00")

    ops_pipeline = client.get("/ops/pipeline-summary", headers=h)
    assert ops_pipeline.status_code == 200
    assert "Comprou" in ops_pipeline.json()["pipeline"]


def test_loss_reason_required_before_marking_lost(client, db_session):
    h = headers(client, db_session)
    lead_id = create_lead(client, h, "Lead Perda")
    blocked = client.patch(f"/leads/{lead_id}/stage", json={"novo_status": "Perdida"}, headers=h)
    assert blocked.status_code == 422

    loss = client.put(f"/leads/{lead_id}/loss-reason", json={"motivo_perda_principal": "Sem dinheiro / orçamento"}, headers=h)
    assert loss.status_code == 200
    missing = client.get("/ops/leads-missing-loss-reason", headers=h)
    assert missing.status_code == 200
    assert missing.json()["count"] == 0
