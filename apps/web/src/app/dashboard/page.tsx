import { SummaryCards, type DashboardSummary } from "@/features/dashboard/summary-cards";
import { fetchDashboardSummary } from "@/lib/api/leads";

export default async function DashboardPage() {
  const { summary, unavailable } = await fetchDashboardSummary<DashboardSummary>();
  return <main className="min-h-screen bg-zinc-50 px-6 py-10"><section className="mx-auto max-w-6xl space-y-6"><header className="space-y-2"><h1 className="text-3xl font-semibold tracking-tight text-zinc-950">Dashboard operacional</h1><p className="text-sm text-zinc-600">Métricas mínimas de leads, qualificação, agendamentos, compras, ticket médio e perdas.</p></header>{unavailable ? <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">API indisponível ou token não configurado.</div> : null}<SummaryCards summary={summary}/></section></main>;
}
