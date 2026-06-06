from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class LossReason(Base):
    __tablename__ = "loss_reasons"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    motivo_perda_principal: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    motivo_perda_secundario: Mapped[str | None] = mapped_column(String(255), nullable=True)
    detalhe_livre: Mapped[str | None] = mapped_column(Text, nullable=True)
    registrado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
