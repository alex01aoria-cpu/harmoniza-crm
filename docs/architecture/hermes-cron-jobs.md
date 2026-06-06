# Cron jobs Hermes — governança CRM

Rotinas recomendadas:
- Resumo diário: rodar `infra/scripts/daily_ops_summary.py` todo dia útil.
- Follow-ups vencidos: rodar `infra/scripts/audit_followups.py` de hora em hora.
- Perdas sem motivo: rodar `infra/scripts/audit_missing_loss_reasons.py` diariamente.

Entrega alvo: Telegram/origin para o operador responsável.
