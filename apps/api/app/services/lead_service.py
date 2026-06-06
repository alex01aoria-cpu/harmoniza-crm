from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead import LeadWithSourceCreate


class LeadService:
    def __init__(self, db: Session) -> None:
        self.repository = LeadRepository(db)

    def create_manual_lead(self, payload: LeadWithSourceCreate) -> Lead:
        return self.repository.create_with_source(payload)
