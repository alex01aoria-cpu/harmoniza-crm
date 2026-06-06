from decimal import Decimal
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.lead import Lead
from app.models.lead_outcome import LeadOutcome
from app.models.loss_reason import LossReason
from app.schemas.dashboard import DashboardSummary
from app.services.auth_service import AuthService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
security = HTTPBearer()

@router.get("/summary", response_model=DashboardSummary)
def summary(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    AuthService.decode_access_token(credentials.credentials)
    leads = db.query(Lead).all()
    outcomes = db.query(LeadOutcome).all()
    losses = db.query(LossReason).all()
    pipeline: dict[str, int] = {}
    for lead in leads: pipeline[lead.status_atual] = pipeline.get(lead.status_atual, 0) + 1
    perdas_por_motivo: dict[str, int] = {}
    for loss in losses: perdas_por_motivo[loss.motivo_perda_principal] = perdas_por_motivo.get(loss.motivo_perda_principal, 0) + 1
    purchases = [o for o in outcomes if o.comprou]
    values = [o.valor_venda for o in purchases if o.valor_venda is not None]
    ticket = (sum(values) / Decimal(len(values))) if values else None
    return DashboardSummary(
        leads_total=len(leads), qualificados=sum(1 for l in leads if l.qualificacao == "Qualificada"),
        agendamentos=sum(1 for o in outcomes if o.agendou), compras=len(purchases), ticket_medio=ticket,
        perdas=len(losses), perdas_por_motivo=perdas_por_motivo, pipeline=pipeline,
    )
