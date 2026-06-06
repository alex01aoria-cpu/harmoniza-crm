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


class LeadRead(LeadBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class LeadWithSourceRead(LeadRead):
    source: LeadSourceRead | None = None
