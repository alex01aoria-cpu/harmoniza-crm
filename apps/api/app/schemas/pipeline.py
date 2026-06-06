from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.schemas.lead import LeadWithSourceRead

PipelineStatus = Literal[
    "Lead nova",
    "Resposta enviada",
    "Respondeu",
    "Triagem em andamento",
    "Triagem concluída",
    "Qualificada",
    "Não qualificada",
    "Passada para vendedora",
    "Agendamento em aberto",
    "Agendou",
    "Compareceu",
    "Comprou",
    "Não comprou",
    "Follow-up",
    "Perdida",
]


class PipelineTransitionRequest(BaseModel):
    novo_status: PipelineStatus
    responsavel_atual: str | None = None
    observacao: str | None = None


class PipelineStageHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    status_origem: str
    status_destino: str
    alterado_por: str
    observacao: str | None = None
    changed_at: datetime


class PipelineTransitionResponse(BaseModel):
    lead: LeadWithSourceRead
    history: PipelineStageHistoryRead
