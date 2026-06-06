from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LeadSourceBase(BaseModel):
    canal: str = Field(min_length=1)
    origem: str | None = None
    campanha: str | None = None
    conjunto: str | None = None
    anuncio: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None
    landing_origem: str | None = None


class LeadSourceInput(LeadSourceBase):
    pass


class LeadSourceCreate(LeadSourceBase):
    lead_id: int


class LeadSourceRead(LeadSourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    capturado_em: datetime
