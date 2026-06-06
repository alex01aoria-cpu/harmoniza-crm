from datetime import UTC, datetime

from app.repositories.lead_repository import LeadRepository


def test_create_and_read_lead(db_session) -> None:
    from app.schemas.lead import LeadCreate

    repository = LeadRepository(db_session)
    payload = LeadCreate(
        nome="Maria Silva",
        telefone="47999990000",
        canal_principal="WhatsApp",
        procedimento_entrada="Skinbooster",
        objetivo_principal="Melhorar textura da pele",
        interesse_principal="Skinbooster",
        duvida_principal="Preço e duração",
        conhece_clinica=True,
        conhece_procedimento=False,
        ja_fez_estetica=True,
        historico_estetico_curto="Já fez limpeza de pele",
        temperatura="Morna",
        qualificacao="Em análise",
        status_atual="Lead nova",
        responsavel_atual="Hermes / Triagem",
        resumo_atual="Lead chegou via campanha de skinbooster",
        proxima_acao="Enviar mensagem inicial",
        data_proxima_acao=datetime(2026, 6, 7, 12, 0, tzinfo=UTC),
    )

    created = repository.create(payload)
    loaded = repository.get_by_id(created.id)

    assert created.id is not None
    assert loaded is not None
    assert loaded.nome == "Maria Silva"
    assert loaded.telefone == "47999990000"
    assert loaded.status_atual == "Lead nova"
    assert loaded.responsavel_atual == "Hermes / Triagem"
    assert loaded.proxima_acao == "Enviar mensagem inicial"
