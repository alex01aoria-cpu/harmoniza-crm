def test_persist_lead_with_source(db_session) -> None:
    from app.models.lead import Lead
    from app.models.lead_source import LeadSource

    lead = Lead(
        nome="Ana Costa",
        telefone="47988887777",
        canal_principal="WhatsApp",
        procedimento_entrada="Preenchimento labial",
        objetivo_principal="Volume labial",
        interesse_principal="Preenchimento labial",
        duvida_principal="Tempo de recuperação",
        conhece_clinica=False,
        conhece_procedimento=True,
        ja_fez_estetica=False,
        temperatura="Quente",
        qualificacao="Qualificada",
        status_atual="Qualificada",
        responsavel_atual="Pré-venda humana",
        resumo_atual="Lead respondeu rapidamente",
        proxima_acao="Passar para vendedora",
    )
    db_session.add(lead)
    db_session.flush()

    source = LeadSource(
        lead_id=lead.id,
        canal="Meta Ads",
        origem="Campanha Meta",
        campanha="Campanha Pr. Labial 11",
        conjunto="Mulheres 25-44 SC",
        anuncio="Vídeo depoimento 03",
        utm_source="meta",
        utm_medium="paid_social",
        utm_campaign="pr_labial_11",
        utm_content="video_03",
        utm_term="harmonizacao_labial",
        landing_origem="lp-preenchimento-labial",
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)
    db_session.refresh(lead)

    assert source.id is not None
    assert source.lead_id == lead.id
    assert lead.source is not None
    assert lead.source.campanha == "Campanha Pr. Labial 11"
    assert lead.source.utm_campaign == "pr_labial_11"
    assert lead.source.anuncio == "Vídeo depoimento 03"
