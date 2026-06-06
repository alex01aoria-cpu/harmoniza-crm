from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class LeadTask(Base):
    __tablename__ = "lead_tasks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao_curta: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsavel: Mapped[str] = mapped_column(String(100), nullable=False)
    data_limite: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status_tarefa: Mapped[str] = mapped_column(String(50), default="Aberta", nullable=False, index=True)
    prioridade: Mapped[str] = mapped_column(String(50), default="Média", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    concluido_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
