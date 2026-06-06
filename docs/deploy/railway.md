# Deploy Railway — Harmoniza CRM V1

Este guia sobe a V1 interna do CRM da Harmoniza no Railway com 3 serviços:

1. PostgreSQL
2. API FastAPI
3. Web Next.js

## Pré-requisitos

- Conta Railway criada.
- Repositório publicado no GitHub.
- Projeto local com branch `main` atualizada.

## Serviço 1 — PostgreSQL

No Railway:

1. `New Project`
2. `Add PostgreSQL`
3. Abra o serviço PostgreSQL e copie a variável `DATABASE_URL`.

## Serviço 2 — API

Crie um novo serviço a partir do GitHub usando o mesmo repositório.

Configuração do serviço:

- Root directory: `apps/api`
- Build command: `uv sync --frozen --no-dev`
- Start command:

```bash
uv run alembic upgrade head && uv run python scripts/bootstrap_admin.py && uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Variáveis obrigatórias:

```text
DATABASE_URL=<DATABASE_URL do PostgreSQL Railway>
ENVIRONMENT=production
SECRET_KEY=<chave longa com mais de 32 caracteres>
ACCESS_TOKEN_EXPIRE_MINUTES=1440
JWT_ALGORITHM=HS256
ADMIN_EMAIL=<email admin>
ADMIN_PASSWORD=<senha forte>
ADMIN_FULL_NAME=Admin Harmoniza
```

Variável para CORS, após criar o frontend:

```text
CORS_ORIGINS=https://url-do-frontend.railway.app
```

Validação da API:

```text
https://url-do-backend.railway.app/health
https://url-do-backend.railway.app/docs
```

## Serviço 3 — Web

Crie outro serviço a partir do mesmo repositório.

Configuração do serviço:

- Root directory: `apps/web`
- Build command: `npm ci && npm run build`
- Start command:

```bash
npm run start -- --hostname 0.0.0.0 --port $PORT
```

Variáveis obrigatórias:

```text
HARMONIZA_CRM_API_URL=https://url-do-backend.railway.app
HARMONIZA_CRM_API_EMAIL=<mesmo ADMIN_EMAIL>
HARMONIZA_CRM_API_PASSWORD=<mesma ADMIN_PASSWORD>
```

Alternativa: usar `HARMONIZA_CRM_API_TOKEN`, mas não é recomendado para beta porque o token expira.

## Ordem correta

1. Criar PostgreSQL.
2. Criar API.
3. Configurar variáveis da API.
4. Deploy da API.
5. Validar `/health`.
6. Criar Web.
7. Configurar variáveis da Web.
8. Deploy da Web.
9. Atualizar `CORS_ORIGINS` da API com a URL final da Web.
10. Redeploy da API.

## Checklist beta interna

- [ ] `/health` da API responde `status: ok`.
- [ ] `/docs` da API abre.
- [ ] Usuário admin consegue autenticar em `/auth/login`.
- [ ] `/leads` carrega sem aviso de API indisponível.
- [ ] `/pipeline` mostra leads por estágio.
- [ ] Atualização de estágio no pipeline grava no backend.
- [ ] `/dashboard` carrega resumo.
- [ ] `/tasks` carrega follow-ups.

## Observações operacionais

- O script `scripts/bootstrap_admin.py` cria ou atualiza o usuário admin no start da API quando `ADMIN_EMAIL` e `ADMIN_PASSWORD` estão definidos.
- Em produção, troque `ADMIN_PASSWORD` depois da primeira validação se ela tiver sido compartilhada em canal inseguro.
- O frontend chama a API pelo servidor Next.js usando `HARMONIZA_CRM_API_EMAIL` e `HARMONIZA_CRM_API_PASSWORD`; essas variáveis não são públicas no browser.
