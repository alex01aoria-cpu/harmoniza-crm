import Link from "next/link";
import { LeadSourceCard } from "@/features/leads/lead-source-card";
import { LeadSummaryCard } from "@/features/leads/lead-summary-card";
import { OutcomeForm } from "@/features/leads/outcome-form";
import { TriageForm } from "@/features/leads/triage-form";
import { fetchLead } from "@/lib/api/leads";

export default async function LeadDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const { lead, unavailable } = await fetchLead(Number(id));
  return <main className="min-h-screen bg-zinc-50 px-6 py-10 text-zinc-950"><section className="mx-auto max-w-5xl space-y-6"><Link href="/leads" className="text-sm font-medium text-zinc-600 hover:text-zinc-950">← Voltar para inbox</Link><header><h1 className="text-3xl font-semibold">Ficha da lead</h1><p className="mt-2 text-sm text-zinc-600">Ficha única com dados, origem, triagem, próxima ação e resultado.</p></header>{unavailable || !lead ? <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">Lead indisponível ou API/token não configurado.</div> : <><LeadSummaryCard lead={lead}/><LeadSourceCard lead={lead}/><TriageForm leadId={lead.id}/><OutcomeForm leadId={lead.id}/></>}</section></main>;
}
