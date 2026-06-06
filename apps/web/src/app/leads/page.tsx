import { LeadsTable } from "@/features/leads/leads-table";
import { fetchLeads } from "@/lib/api/leads";

type LeadsPageProps = {
  searchParams: Promise<{
    status_atual?: string;
    campanha?: string;
  }>;
};

export default async function LeadsPage({ searchParams }: LeadsPageProps) {
  const filters = await searchParams;
  const { leads, unavailable } = await fetchLeads({
    status_atual: filters.status_atual,
    campanha: filters.campanha,
    limit: 50,
  });

  return (
    <main className="min-h-screen bg-zinc-50 px-6 py-10 text-zinc-950">
      <section className="mx-auto max-w-7xl space-y-6">
        <header className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
          <div className="space-y-2">
            <span className="inline-flex rounded-full bg-zinc-900 px-3 py-1 text-xs font-medium uppercase tracking-wide text-white">
              Inbox operacional
            </span>
            <h1 className="text-3xl font-semibold tracking-tight text-zinc-950">
              Novos leads
            </h1>
            <p className="max-w-3xl text-sm leading-6 text-zinc-600">
              Visão rápida das entradas recentes para triagem, handoff comercial e
              cobrança de próxima ação. Mostra origem, campanha, status,
              responsável e horário de entrada.
            </p>
          </div>

          <form className="grid gap-3 rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm sm:grid-cols-3">
            <label className="space-y-1 text-xs font-medium text-zinc-600">
              Status
              <input
                name="status_atual"
                defaultValue={filters.status_atual ?? ""}
                placeholder="Lead nova"
                className="w-full rounded-xl border border-zinc-300 px-3 py-2 text-sm text-zinc-950 outline-none transition focus:border-zinc-900"
              />
            </label>
            <label className="space-y-1 text-xs font-medium text-zinc-600">
              Campanha
              <input
                name="campanha"
                defaultValue={filters.campanha ?? ""}
                placeholder="Camp Skinbooster 8"
                className="w-full rounded-xl border border-zinc-300 px-3 py-2 text-sm text-zinc-950 outline-none transition focus:border-zinc-900"
              />
            </label>
            <div className="flex items-end">
              <button
                type="submit"
                className="w-full rounded-xl bg-zinc-950 px-4 py-2 text-sm font-medium text-white transition hover:bg-zinc-800"
              >
                Filtrar
              </button>
            </div>
          </form>
        </header>

        {unavailable ? (
          <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
            API indisponível ou token não configurado. Configure
            <code className="mx-1 rounded bg-amber-100 px-1 py-0.5">
              HARMONIZA_CRM_API_URL
            </code>
            e
            <code className="mx-1 rounded bg-amber-100 px-1 py-0.5">
              HARMONIZA_CRM_API_TOKEN
            </code>
            para carregar dados reais.
          </div>
        ) : null}

        <LeadsTable leads={leads} />
      </section>
    </main>
  );
}
