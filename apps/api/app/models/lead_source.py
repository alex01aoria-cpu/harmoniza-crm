from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class LeadSource(Base):
    __tablename__ = "lead_sources"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    canal: Mapped[str] = mapped_column(String(100), nullable=False)
    origem: Mapped[str | None] = mapped_column(String(255), nullable=True)
    campanha: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    conjunto: Mapped[str | None] = mapped_column(String(255), nullable=True)
    anuncio: Mapped[str | None] = mapped_column(String(255), nullable=True)
    utm_source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    utm_medium: Mapped[str | None] = mapped_column(String(255), nullable=True)
    utm_campaign: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    utm_content: Mapped[str | None] = mapped_column(String(255), nullable=True)
    utm_term: Mapped[str | None] = mapped_column(String(255), nullable=True)
    landing_origem: Mapped[str | None] = mapped_column(String(255), nullable=True)
    capturado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    lead: Mapped["Lead"] = relationship(back_populates="source")

    def __repr__(self) -> str:
        return f"LeadSource(id={self.id!r}, lead_id={self.lead_id!r}, canal={self.canal!r})"
