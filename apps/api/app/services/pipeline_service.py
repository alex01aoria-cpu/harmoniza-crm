from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.models.pipeline_stage_history import PipelineStageHistory
from app.models.loss_reason import LossReason
from app.schemas.pipeline import PipelineTransitionRequest


class PipelineService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def transition_stage(
        self,
        *,
        lead_id: int,
        payload: PipelineTransitionRequest,
        alterado_por: str,
    ) -> tuple[Lead, PipelineStageHistory]:
        lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
        if lead is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead not found",
            )

        if payload.novo_status == "Perdida":
            loss = self.db.query(LossReason).filter(LossReason.lead_id == lead_id).first()
            if loss is None:
                raise HTTPException(status_code=422, detail="Loss reason required before marking lead as lost")

        status_origem = lead.status_atual
        lead.status_atual = payload.novo_status
        if payload.responsavel_atual is not None:
            lead.responsavel_atual = payload.responsavel_atual

        history = PipelineStageHistory(
            lead_id=lead.id,
            status_origem=status_origem,
            status_destino=payload.novo_status,
            alterado_por=alterado_por,
            observacao=payload.observacao,
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(lead)
        self.db.refresh(history)
        return lead, history
