# E2E — lead até compra
1. POST /leads.
2. POST /leads/{id}/handoff.
3. POST /tasks para follow-up.
4. PUT /leads/{id}/outcome com comprou=true e valor.
5. GET /dashboard/summary reflete compra e ticket médio.
