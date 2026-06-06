from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.lead import Lead
from app.models.lead_outcome import LeadOutcome
from app.models.loss_reason import LossReason
from app.schemas.outcomes import LeadOutcomeRead, LeadOutcomeUpsert, LossReasonRead, LossReasonUpsert
from app.services.auth_service import AuthService

router = APIRouter(prefix="/leads", tags=["outcomes"])
security = HTTPBearer()

@router.put("/{lead_id}/outcome", response_model=LeadOutcomeRead)
def upsert_outcome(lead_id: int, payload: LeadOutcomeUpsert, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    AuthService.decode_access_token(credentials.credentials)
    outcome = db.query(LeadOutcome).filter(LeadOutcome.lead_id == lead_id).first()
    if outcome is None:
        outcome = LeadOutcome(lead_id=lead_id); db.add(outcome)
    for k, v in payload.model_dump().items(): setattr(outcome, k, v)
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if lead and payload.comprou: lead.status_atual = "Comprou"
    elif lead and payload.compareceu: lead.status_atual = "Compareceu"
    elif lead and payload.agendou: lead.status_atual = "Agendou"
    db.commit(); db.refresh(outcome)
    return outcome

@router.put("/{lead_id}/loss-reason", response_model=LossReasonRead)
def upsert_loss_reason(lead_id: int, payload: LossReasonUpsert, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    AuthService.decode_access_token(credentials.credentials)
    reason = db.query(LossReason).filter(LossReason.lead_id == lead_id).first()
    if reason is None:
        reason = LossReason(lead_id=lead_id); db.add(reason)
    for k, v in payload.model_dump().items(): setattr(reason, k, v)
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if lead: lead.status_atual = "Perdida"
    db.commit(); db.refresh(reason)
    return reason
