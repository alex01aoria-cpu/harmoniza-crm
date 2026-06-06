from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.models.lead_source import LeadSource
from app.schemas.lead import LeadCreate, LeadWithSourceCreate


class LeadRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: LeadCreate) -> Lead:
        lead = Lead(**payload.model_dump())
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def create_with_source(self, payload: LeadWithSourceCreate) -> Lead:
        data = payload.model_dump(exclude={"source"})
        lead = Lead(**data)
        self.db.add(lead)
        self.db.flush()

        if payload.source is not None:
            source = LeadSource(lead_id=lead.id, **payload.source.model_dump())
            self.db.add(source)

        self.db.commit()
        self.db.refresh(lead)
        return lead

    def get_by_id(self, lead_id: int) -> Lead | None:
        return self.db.query(Lead).filter(Lead.id == lead_id).first()
