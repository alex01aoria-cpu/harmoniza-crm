# E2E — lead rastreada até pipeline
1. POST /lead-capture com UTMs.
2. Login.
3. GET /leads confirma entrada no inbox.
4. PATCH /leads/{id}/stage move estágio.
5. GET /ops/pipeline-summary reflete movimento.
