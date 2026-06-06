from decimal import Decimal
from pydantic import BaseModel

class DashboardSummary(BaseModel):
    leads_total: int
    qualificados: int
    agendamentos: int
    compras: int
    ticket_medio: Decimal | None
    perdas: int
    perdas_por_motivo: dict[str, int]
    pipeline: dict[str, int]
