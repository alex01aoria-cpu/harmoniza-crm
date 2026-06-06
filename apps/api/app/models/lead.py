from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    telefone: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    canal_principal: Mapped[str] = mapped_column(String(100), nullable=False)
    procedimento_entrada: Mapped[str] = mapped_column(String(255), nullable=False)
    objetivo_principal: Mapped[str | None] = mapped_column(Text, nullable=True)
    interesse_principal: Mapped[str | None] = mapped_column(String(255), nullable=True)
    duvida_principal: Mapped[str | None] = mapped_column(Text, nullable=True)
    conhece_clinica: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    conhece_procedimento: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ja_fez_estetica: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    historico_estetico_curto: Mapped[str | None] = mapped_column(Text, nullable=True)
    temperatura: Mapped[str] = mapped_column(String(50), nullable=False)
    qualificacao: Mapped[str] = mapped_column(String(50), nullable=False)
    status_atual: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    responsavel_atual: Mapped[str] = mapped_column(String(100), nullable=False)
    resumo_atual: Mapped[str | None] = mapped_column(Text, nullable=True)
    proxima_acao: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_proxima_acao: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    source: Mapped["LeadSource | None"] = relationship(
        back_populates="lead",
        cascade="all, delete-orphan",
        uselist=False,
    )

    def __repr__(self) -> str:
        return f"Lead(id={self.id!r}, nome={self.nome!r}, telefone={self.telefone!r})"
