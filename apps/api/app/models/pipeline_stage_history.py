from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.lead import Lead


class PipelineStageHistory(Base):
    __tablename__ = "pipeline_stage_history"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status_origem: Mapped[str] = mapped_column(String(100), nullable=False)
    status_destino: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    alterado_por: Mapped[str] = mapped_column(String(255), nullable=False)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    lead: Mapped["Lead"] = relationship()

    def __repr__(self) -> str:
        return (
            "PipelineStageHistory("
            f"id={self.id!r}, lead_id={self.lead_id!r}, "
            f"status_origem={self.status_origem!r}, "
            f"status_destino={self.status_destino!r})"
        )
