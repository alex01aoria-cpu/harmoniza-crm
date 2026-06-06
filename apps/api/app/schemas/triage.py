from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TriageUpdate(BaseModel):
    objetivo_principal: str | None = None
    interesse_principal: str | None = None
    duvida_principal: str | None = None
    conhece_clinica: bool | None = None
    conhece_procedimento: bool | None = None
    ja_fez_estetica: bool | None = None
    historico_estetico_curto: str | None = None
    temperatura: str | None = None
    qualificacao: str | None = None
    resumo_atual: str | None = None
    proxima_acao: str | None = None
    data_proxima_acao: datetime | None = None

class HandoffRequest(BaseModel):
    responsavel_atual: str
    resumo_atual: str
    proxima_acao: str
