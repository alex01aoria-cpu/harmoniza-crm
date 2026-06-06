import type { Lead } from "@/lib/api/leads";
import { PIPELINE_STATUSES } from "@/lib/api/leads";

type KanbanColumnProps = {
  status: string;
  leads: Lead[];
  transitionAction: (formData: FormData) => Promise<void>;
};

function toneForTemperature(temperature: string) {
  if (temperature === "Quente") return "bg-red-50 text-red-700 ring-red-200";
  if (temperature === "Morna") return "bg-amber-50 text-amber-700 ring-amber-200";
  return "bg-sky-50 text-sky-700 ring-sky-200";
}

export function KanbanColumn({ status, leads, transitionAction }: KanbanColumnProps) {
  return (
    <section className="flex min-h-[32rem] w-80 shrink-0 flex-col rounded-2xl border border-zinc-200 bg-zinc-100/70 shadow-sm">
      <header className="flex items-center justify-between border-b border-zinc-200 px-4 py-3">
        <h2 className="text-sm font-semibold text-zinc-950">{status}</h2>
        <span className="rounded-full bg-white px-2 py-1 text-xs font-medium text-zinc-600 ring-1 ring-zinc-200">
          {leads.length}
        </span>
      </header>

      <div className="flex flex-1 flex-col gap-3 overflow-y-auto p-3">
        {leads.length === 0 ? (
          <div className="rounded-xl border border-dashed border-zinc-300 bg-white/70 p-4 text-xs text-zinc-500">
            Sem leads neste estágio.
          </div>
        ) : null}

        {leads.map((lead) => (
          <article key={lead.id} className="rounded-xl border border-zinc-200 bg-white p-4 shadow-sm">
            <div className="space-y-2">
              <div>
                <h3 className="font-medium text-zinc-950">{lead.nome}</h3>
                <p className="text-xs text-zinc-500">{lead.telefone}</p>
              </div>
              <p className="text-xs text-zinc-600">{lead.procedimento_entrada}</p>
              <div className="flex flex-wrap gap-2">
                <span className={`rounded-full px-2 py-1 text-xs font-medium ring-1 ${toneForTemperature(lead.temperatura)}`}>
                  {lead.temperatura}
                </span>
                <span className="rounded-full bg-zinc-100 px-2 py-1 text-xs font-medium text-zinc-700 ring-1 ring-zinc-200">
                  {lead.responsavel_atual}
                </span>
              </div>
              <div className="rounded-lg bg-zinc-50 p-2 text-xs text-zinc-600">
                <div>{lead.source?.campanha ?? "Sem campanha"}</div>
                <div className="mt-1 text-zinc-400">{lead.source?.canal ?? lead.canal_principal}</div>
              </div>
            </div>

            <form action={transitionAction} className="mt-4 space-y-2 border-t border-zinc-100 pt-3">
              <input type="hidden" name="lead_id" value={lead.id} />
              <label className="block text-xs font-medium text-zinc-600">
                Mover para
                <select
                  name="novo_status"
                  defaultValue={lead.status_atual}
                  className="mt-1 w-full rounded-lg border border-zinc-300 bg-white px-2 py-2 text-xs text-zinc-950 outline-none focus:border-zinc-900"
                >
                  {PIPELINE_STATUSES.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </label>
              <input
                name="observacao"
                placeholder="Observação opcional"
                className="w-full rounded-lg border border-zinc-300 px-2 py-2 text-xs text-zinc-950 outline-none focus:border-zinc-900"
              />
              <button
                type="submit"
                className="w-full rounded-lg bg-zinc-950 px-3 py-2 text-xs font-medium text-white transition hover:bg-zinc-800"
              >
                Atualizar estágio
              </button>
            </form>
          </article>
        ))}
      </div>
    </section>
  );
}
