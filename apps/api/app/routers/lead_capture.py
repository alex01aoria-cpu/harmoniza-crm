from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.lead import LeadCaptureCreate, LeadWithSourceRead
from app.services.lead_service import LeadService

router = APIRouter(prefix="/lead-capture", tags=["lead-capture"])


@router.post("", response_model=LeadWithSourceRead, status_code=status.HTTP_201_CREATED)
def capture_lead(
    payload: LeadCaptureCreate,
    db: Session = Depends(get_db),
) -> LeadWithSourceRead:
    lead = LeadService(db).create_tracked_capture(payload)
    return LeadWithSourceRead.model_validate(lead)
