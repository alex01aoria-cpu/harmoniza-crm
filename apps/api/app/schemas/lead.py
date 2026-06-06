from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LeadBase(BaseModel):
    nome: str
    telefone: str
    canal_principal: str
    procedimento_entrada: str
    objetivo_principal: str | None = None
    interesse_principal: str | None = None
    duvida_principal: str | None = None
    conhece_clinica: bool = False
    conhece_procedimento: bool = False
    ja_fez_estetica: bool = False
    historico_estetico_curto: str | None = None
    temperatura: str
    qualificacao: str
    status_atual: str
    responsavel_atual: str
    resumo_atual: str | None = None
    proxima_acao: str | None = None
    data_proxima_acao: datetime | None = None


class LeadCreate(LeadBase):
    pass


class LeadRead(LeadBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
