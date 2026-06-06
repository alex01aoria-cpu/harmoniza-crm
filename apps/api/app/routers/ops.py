from datetime import datetime, UTC
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.lead import Lead
from app.models.lead_task import LeadTask
from app.models.loss_reason import LossReason
from app.services.auth_service import AuthService

router = APIRouter(prefix="/ops", tags=["ops"])
security = HTTPBearer()

def auth(credentials, db):
    AuthService.decode_access_token(credentials.credentials)

@router.get("/followups-overdue")
def followups_overdue(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    auth(credentials, db)
    tasks = db.query(LeadTask).filter(LeadTask.status_tarefa != "Concluída", LeadTask.data_limite < datetime.now(UTC)).all()
    return {"count": len(tasks), "items": [{"id": t.id, "lead_id": t.lead_id, "titulo": t.titulo, "data_limite": t.data_limite.isoformat()} for t in tasks]}

@router.get("/leads-without-next-action")
def leads_without_next_action(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    auth(credentials, db)
    leads = db.query(Lead).filter((Lead.proxima_acao == None) | (Lead.proxima_acao == "")).all()  # noqa: E711
    return {"count": len(leads), "items": [{"id": l.id, "nome": l.nome, "status_atual": l.status_atual} for l in leads]}

@router.get("/leads-missing-loss-reason")
def leads_missing_loss_reason(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    auth(credentials, db)
    with_loss = {x.lead_id for x in db.query(LossReason).all()}
    leads = [l for l in db.query(Lead).filter(Lead.status_atual == "Perdida").all() if l.id not in with_loss]
    return {"count": len(leads), "items": [{"id": l.id, "nome": l.nome} for l in leads]}

@router.get("/pipeline-summary")
def pipeline_summary(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    auth(credentials, db)
    summary: dict[str, int] = {}
    for lead in db.query(Lead).all(): summary[lead.status_atual] = summary.get(lead.status_atual, 0) + 1
    return {"pipeline": summary}
