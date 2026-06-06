import type { Lead } from "@/lib/api/leads";

type LeadsTableProps = {
  leads: Lead[];
};

function formatDate(value: string | null) {
  if (!value) return "--";
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(value));
}

function statusBadge(status: string) {
  const isNew = status === "Lead nova";
  return isNew
    ? "bg-emerald-50 text-emerald-700 ring-emerald-200"
    : "bg-zinc-100 text-zinc-700 ring-zinc-200";
}

export function LeadsTable({ leads }: LeadsTableProps) {
  if (leads.length === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-zinc-300 bg-white p-8 text-center shadow-sm">
        <p className="text-sm font-medium text-zinc-900">Nenhuma lead encontrada.</p>
        <p className="mt-2 text-sm text-zinc-500">
          Ajuste os filtros ou confirme se a API já recebeu entradas rastreáveis.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-zinc-200 text-sm">
          <thead className="bg-zinc-50 text-left text-xs font-semibold uppercase tracking-wide text-zinc-500">
            <tr>
              <th className="px-5 py-3">Lead</th>
              <th className="px-5 py-3">Origem</th>
              <th className="px-5 py-3">Status</th>
              <th className="px-5 py-3">Responsável</th>
              <th className="px-5 py-3">Temperatura</th>
              <th className="px-5 py-3">Entrada</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100">
            {leads.map((lead) => (
              <tr key={lead.id} className="align-top hover:bg-zinc-50">
                <td className="px-5 py-4">
                  <div className="font-medium text-zinc-950">{lead.nome}</div>
                  <div className="mt-1 text-zinc-500">{lead.telefone}</div>
                  <div className="mt-1 text-xs text-zinc-400">
                    {lead.procedimento_entrada}
                  </div>
                </td>
                <td className="px-5 py-4 text-zinc-700">
                  <div>{lead.source?.campanha ?? "Sem campanha"}</div>
                  <div className="mt-1 text-xs text-zinc-500">
                    {lead.source?.canal ?? lead.canal_principal}
                    {lead.source?.anuncio ? ` · ${lead.source.anuncio}` : ""}
                  </div>
                </td>
                <td className="px-5 py-4">
                  <span
                    className={`inline-flex rounded-full px-2.5 py-1 text-xs font-medium ring-1 ${statusBadge(
                      lead.status_atual,
                    )}`}
                  >
                    {lead.status_atual}
                  </span>
                </td>
                <td className="px-5 py-4 text-zinc-700">{lead.responsavel_atual}</td>
                <td className="px-5 py-4 text-zinc-700">{lead.temperatura}</td>
                <td className="px-5 py-4 text-zinc-500">{formatDate(lead.created_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
