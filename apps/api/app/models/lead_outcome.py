from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class LeadOutcome(Base):
    __tablename__ = "lead_outcomes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    agendou: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    data_agendamento: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    compareceu: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    data_comparecimento: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    comprou: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    data_compra: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    valor_venda: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    observacao_resultado: Mapped[str | None] = mapped_column(Text, nullable=True)
