from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.schemas.lead import LeadCreate


class LeadRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: LeadCreate) -> Lead:
        lead = Lead(**payload.model_dump())
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def get_by_id(self, lead_id: int) -> Lead | None:
        return self.db.query(Lead).filter(Lead.id == lead_id).first()
