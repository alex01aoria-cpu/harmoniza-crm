# Integração Hermes — CRM Harmoniza V1

Variáveis esperadas:
- `HARMONIZA_CRM_API_URL`
- `HARMONIZA_CRM_API_TOKEN`

Endpoints de governança:
- `GET /ops/followups-overdue`
- `GET /ops/leads-without-next-action`
- `GET /ops/leads-missing-loss-reason`
- `GET /ops/pipeline-summary`
- `GET /dashboard/summary`

Scripts em `infra/scripts/` produzem saída curta para cron do Hermes.
