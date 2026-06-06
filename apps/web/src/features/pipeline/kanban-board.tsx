import type { Lead } from "@/lib/api/leads";
import { PIPELINE_STATUSES } from "@/lib/api/leads";
import { KanbanColumn } from "./kanban-column";

type KanbanBoardProps = {
  leads: Lead[];
  transitionAction: (formData: FormData) => Promise<void>;
};

export function KanbanBoard({ leads, transitionAction }: KanbanBoardProps) {
  const leadsByStatus = new Map<string, Lead[]>();
  for (const status of PIPELINE_STATUSES) {
    leadsByStatus.set(status, []);
  }

  for (const lead of leads) {
    const group = leadsByStatus.get(lead.status_atual) ?? [];
    group.push(lead);
    leadsByStatus.set(lead.status_atual, group);
  }

  return (
    <div className="overflow-x-auto pb-4">
      <div className="flex min-w-full gap-4">
        {PIPELINE_STATUSES.map((status) => (
          <KanbanColumn
            key={status}
            status={status}
            leads={leadsByStatus.get(status) ?? []}
            transitionAction={transitionAction}
          />
        ))}
      </div>
    </div>
  );
}
