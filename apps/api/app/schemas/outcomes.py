from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class LeadOutcomeUpsert(BaseModel):
    agendou: bool = False
    data_agendamento: datetime | None = None
    compareceu: bool = False
    data_comparecimento: datetime | None = None
    comprou: bool = False
    data_compra: datetime | None = None
    valor_venda: Decimal | None = None
    observacao_resultado: str | None = None

class LeadOutcomeRead(LeadOutcomeUpsert):
    model_config = ConfigDict(from_attributes=True)
    id: int
    lead_id: int

class LossReasonUpsert(BaseModel):
    motivo_perda_principal: str = Field(min_length=1)
    motivo_perda_secundario: str | None = None
    detalhe_livre: str | None = None

class LossReasonRead(LossReasonUpsert):
    model_config = ConfigDict(from_attributes=True)
    id: int
    lead_id: int
    registrado_em: datetime
