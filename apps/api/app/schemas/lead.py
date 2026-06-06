from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.lead_source import LeadSourceInput, LeadSourceRead


class LeadBase(BaseModel):
    nome: str = Field(min_length=1)
    telefone: str = Field(min_length=8)
    canal_principal: str = Field(min_length=1)
    procedimento_entrada: str = Field(min_length=1)
    objetivo_principal: str | None = None
    interesse_principal: str | None = None
    duvida_principal: str | None = None
    conhece_clinica: bool = False
    conhece_procedimento: bool = False
    ja_fez_estetica: bool = False
    historico_estetico_curto: str | None = None
    temperatura: str = Field(min_length=1)
    qualificacao: str = Field(min_length=1)
    status_atual: str = Field(min_length=1)
    responsavel_atual: str = Field(min_length=1)
    resumo_atual: str | None = None
    proxima_acao: str | None = None
    data_proxima_acao: datetime | None = None


class LeadCreate(LeadBase):
    pass


class LeadWithSourceCreate(LeadBase):
    source: LeadSourceInput | None = None


class LeadCaptureCreate(BaseModel):
    nome: str = Field(min_length=1)
    telefone: str = Field(min_length=8)
    procedimento_entrada: str = Field(min_length=1)
    canal_principal: str = "WhatsApp"
    canal: str = Field(min_length=1)
    origem: str | None = None
    campanha: str | None = None
    conjunto: str | None = None
    anuncio: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None
    landing_origem: str | None = None

    def to_lead_with_source(self) -> LeadWithSourceCreate:
        return LeadWithSourceCreate(
            nome=self.nome,
            telefone=self.telefone,
            canal_principal=self.canal_principal,
            procedimento_entrada=self.procedimento_entrada,
            temperatura="Fria",
            qualificacao="Em análise",
            status_atual="Lead nova",
            responsavel_atual="Hermes / Triagem",
            resumo_atual="Lead capturada com origem rastreável",
            proxima_acao="Iniciar triagem no WhatsApp",
            source=LeadSourceInput(
                canal=self.canal,
                origem=self.origem,
                campanha=self.campanha,
                conjunto=self.conjunto,
                anuncio=self.anuncio,
                utm_source=self.utm_source,
                utm_medium=self.utm_medium,
                utm_campaign=self.utm_campaign,
                utm_content=self.utm_content,
                utm_term=self.utm_term,
                landing_origem=self.landing_origem,
            ),
        )


class LeadRead(LeadBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class LeadWithSourceRead(LeadRead):
    source: LeadSourceRead | None = None
