from datetime import datetime, UTC
from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.lead_task import LeadTask
from app.schemas.tasks import LeadTaskCreate, LeadTaskRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/tasks", tags=["tasks"])
security = HTTPBearer()

@router.post("", response_model=LeadTaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: LeadTaskCreate, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    AuthService.decode_access_token(credentials.credentials)
    task = LeadTask(**payload.model_dump())
    db.add(task); db.commit(); db.refresh(task)
    return task

@router.get("", response_model=list[LeadTaskRead])
def list_tasks(status_tarefa: str | None = None, overdue: bool = False, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    AuthService.decode_access_token(credentials.credentials)
    q = db.query(LeadTask)
    if status_tarefa: q = q.filter(LeadTask.status_tarefa == status_tarefa)
    if overdue: q = q.filter(LeadTask.status_tarefa != "Concluída", LeadTask.data_limite < datetime.now(UTC))
    return q.order_by(LeadTask.data_limite.asc()).limit(100).all()
