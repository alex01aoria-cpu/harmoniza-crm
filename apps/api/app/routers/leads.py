from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.lead import LeadWithSourceCreate, LeadWithSourceRead
from app.schemas.triage import TriageUpdate, HandoffRequest
from app.schemas.pipeline import (
    PipelineTransitionRequest,
    PipelineTransitionResponse,
    PipelineStageHistoryRead,
)
from app.services.auth_service import AuthService
from app.services.lead_service import LeadService
from app.services.pipeline_service import PipelineService

router = APIRouter(prefix="/leads", tags=["leads"])
security = HTTPBearer()


@router.get("", response_model=list[LeadWithSourceRead])
def list_leads(
    status_atual: str | None = None,
    campanha: str | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> list[LeadWithSourceRead]:
    AuthService.decode_access_token(credentials.credentials)
    leads = LeadService(db).list_recent_leads(
        status_atual=status_atual,
        campanha=campanha,
        limit=limit,
    )
    return [LeadWithSourceRead.model_validate(lead) for lead in leads]


@router.get("/{lead_id}", response_model=LeadWithSourceRead)
def get_lead(
    lead_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> LeadWithSourceRead:
    from fastapi import HTTPException
    AuthService.decode_access_token(credentials.credentials)
    lead = LeadService(db).repository.get_by_id(lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return LeadWithSourceRead.model_validate(lead)


@router.patch("/{lead_id}/triage", response_model=LeadWithSourceRead)
def update_triage(
    lead_id: int,
    payload: TriageUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> LeadWithSourceRead:
    from fastapi import HTTPException
    AuthService.decode_access_token(credentials.credentials)
    lead = LeadService(db).update_triage(lead_id, payload)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return LeadWithSourceRead.model_validate(lead)


@router.post("/{lead_id}/handoff", response_model=PipelineTransitionResponse)
def handoff_lead(
    lead_id: int,
    payload: HandoffRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> PipelineTransitionResponse:
    alterado_por = AuthService.decode_access_token(credentials.credentials)
    lead_service = LeadService(db)
    lead = lead_service.update_triage(
        lead_id,
        TriageUpdate(
            resumo_atual=payload.resumo_atual,
            proxima_acao=payload.proxima_acao,
        ),
    )
    if lead is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Lead not found")
    transition = PipelineTransitionRequest(
        novo_status="Passada para vendedora",
        responsavel_atual=payload.responsavel_atual,
        observacao=payload.resumo_atual,
    )
    lead, history = PipelineService(db).transition_stage(lead_id=lead_id, payload=transition, alterado_por=alterado_por)
    return PipelineTransitionResponse(lead=LeadWithSourceRead.model_validate(lead), history=PipelineStageHistoryRead.model_validate(history))


@router.patch("/{lead_id}/stage", response_model=PipelineTransitionResponse)
def transition_stage(
    lead_id: int,
    payload: PipelineTransitionRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> PipelineTransitionResponse:
    alterado_por = AuthService.decode_access_token(credentials.credentials)
    lead, history = PipelineService(db).transition_stage(
        lead_id=lead_id,
        payload=payload,
        alterado_por=alterado_por,
    )
    return PipelineTransitionResponse(
        lead=LeadWithSourceRead.model_validate(lead),
        history=PipelineStageHistoryRead.model_validate(history),
    )


@router.post("", response_model=LeadWithSourceRead, status_code=status.HTTP_201_CREATED)
def create_lead(
    payload: LeadWithSourceCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> LeadWithSourceRead:
    AuthService.decode_access_token(credentials.credentials)
    lead = LeadService(db).create_manual_lead(payload)
    return LeadWithSourceRead.model_validate(lead)
