from app.models.lead import Lead
from app.models.lead_source import LeadSource


def test_tracked_lead_capture_creates_preliminary_lead_with_source(client, db_session) -> None:
    response = client.post(
        "/lead-capture",
        json={
            "nome": "Fernanda Oliveira",
            "telefone": "47977776666",
            "procedimento_entrada": "Skinbooster",
            "canal_principal": "WhatsApp",
            "canal": "Meta Ads",
            "origem": "Landing Page Skinbooster",
            "campanha": "Camp Skinbooster 8",
            "conjunto": "Mulheres 25-40 SC",
            "anuncio": "Criativo Pele Glow 02",
            "utm_source": "meta",
            "utm_medium": "paid_social",
            "utm_campaign": "skinbooster_8",
            "utm_content": "pele_glow_02",
            "utm_term": "skinbooster",
            "landing_origem": "lp-skinbooster",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] is not None
    assert body["nome"] == "Fernanda Oliveira"
    assert body["status_atual"] == "Lead nova"
    assert body["responsavel_atual"] == "Hermes / Triagem"
    assert body["qualificacao"] == "Em análise"
    assert body["source"]["campanha"] == "Camp Skinbooster 8"
    assert body["source"]["utm_campaign"] == "skinbooster_8"

    saved_lead = db_session.query(Lead).filter(Lead.id == body["id"]).first()
    saved_source = (
        db_session.query(LeadSource)
        .filter(LeadSource.lead_id == body["id"])
        .first()
    )

    assert saved_lead is not None
    assert saved_source is not None
    assert saved_source.anuncio == "Criativo Pele Glow 02"
    assert saved_source.landing_origem == "lp-skinbooster"


def test_tracked_lead_capture_requires_minimum_contact_data(client) -> None:
    response = client.post(
        "/lead-capture",
        json={
            "nome": "Lead sem telefone",
            "procedimento_entrada": "Botox",
            "canal": "Meta Ads",
        },
    )

    assert response.status_code == 422
