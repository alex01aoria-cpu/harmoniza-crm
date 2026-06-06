from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead import LeadCaptureCreate, LeadWithSourceCreate


class LeadService:
    def __init__(self, db: Session) -> None:
        self.repository = LeadRepository(db)

    def create_manual_lead(self, payload: LeadWithSourceCreate) -> Lead:
        return self.repository.create_with_source(payload)

    def create_tracked_capture(self, payload: LeadCaptureCreate) -> Lead:
        return self.repository.create_with_source(payload.to_lead_with_source())

    def list_recent_leads(
        self,
        *,
        status_atual: str | None = None,
        campanha: str | None = None,
        limit: int = 50,
    ) -> list[Lead]:
        return self.repository.list_recent(
            status_atual=status_atual,
            campanha=campanha,
            limit=limit,
        )
