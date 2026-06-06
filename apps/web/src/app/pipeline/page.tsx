import Link from "next/link";
import { revalidatePath } from "next/cache";

import { KanbanBoard } from "@/features/pipeline/kanban-board";
import { fetchLeads, updateLeadStage } from "@/lib/api/leads";

async function transitionLeadStage(formData: FormData) {
  "use server";

  const leadId = Number(formData.get("lead_id"));
  const novoStatus = String(formData.get("novo_status") ?? "");
  const observacao = String(formData.get("observacao") ?? "").trim();

  if (!leadId || !novoStatus) return;

  await updateLeadStage(leadId, {
    novo_status: novoStatus,
    observacao: observacao || undefined,
  });
  revalidatePath("/pipeline");
  revalidatePath("/leads");
}

export default async function PipelinePage() {
  const { leads, unavailable } = await fetchLeads({ limit: 100 });

  return (
    <main className="min-h-screen bg-zinc-50 px-6 py-10 text-zinc-950">
      <section className="mx-auto max-w-[96rem] space-y-6">
        <header className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
          <div className="space-y-2">
            <span className="inline-flex rounded-full bg-zinc-900 px-3 py-1 text-xs font-medium uppercase tracking-wide text-white">
              Kanban comercial
            </span>
            <h1 className="text-3xl font-semibold tracking-tight text-zinc-950">
              Pipeline de pré-venda
            </h1>
            <p className="max-w-3xl text-sm leading-6 text-zinc-600">
              Visão visual dos status oficiais da V1. Cada card mostra lead,
              origem, temperatura e responsável. A ação de mudança de estágio
              chama o backend e registra histórico.
            </p>
          </div>

          <Link
            href="/leads"
            className="inline-flex items-center justify-center rounded-xl border border-zinc-300 bg-white px-4 py-2 text-sm font-medium text-zinc-900 shadow-sm transition hover:bg-zinc-100"
          >
            Voltar para inbox
          </Link>
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
            para carregar e mover cards reais.
          </div>
        ) : null}

        <KanbanBoard leads={leads} transitionAction={transitionLeadStage} />
      </section>
    </main>
  );
}
