from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class LeadTaskCreate(BaseModel):
    lead_id: int
    titulo: str = Field(min_length=1)
    descricao_curta: str | None = None
    responsavel: str = Field(min_length=1)
    data_limite: datetime
    status_tarefa: str = "Aberta"
    prioridade: str = "Média"

class LeadTaskRead(LeadTaskCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    concluido_em: datetime | None = None
