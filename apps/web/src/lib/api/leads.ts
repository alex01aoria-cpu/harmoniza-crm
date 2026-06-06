export type LeadSource = {
  id: number;
  lead_id: number;
  canal: string;
  origem: string | null;
  campanha: string | null;
  conjunto: string | null;
  anuncio: string | null;
  utm_source: string | null;
  utm_medium: string | null;
  utm_campaign: string | null;
  utm_content: string | null;
  utm_term: string | null;
  landing_origem: string | null;
  capturado_em: string;
};

export type Lead = {
  id: number;
  nome: string;
  telefone: string;
  canal_principal: string;
  procedimento_entrada: string;
  objetivo_principal: string | null;
  interesse_principal: string | null;
  duvida_principal: string | null;
  conhece_clinica: boolean;
  conhece_procedimento: boolean;
  ja_fez_estetica: boolean;
  historico_estetico_curto: string | null;
  temperatura: string;
  qualificacao: string;
  status_atual: string;
  responsavel_atual: string;
  resumo_atual: string | null;
  proxima_acao: string | null;
  data_proxima_acao: string | null;
  created_at: string;
  updated_at: string;
  source: LeadSource | null;
};

export type LeadsFilters = {
  status_atual?: string;
  campanha?: string;
  limit?: number;
};

export type LeadsResult = {
  leads: Lead[];
  unavailable: boolean;
};

export const PIPELINE_STATUSES = [
  "Lead nova",
  "Resposta enviada",
  "Respondeu",
  "Triagem em andamento",
  "Triagem concluída",
  "Qualificada",
  "Não qualificada",
  "Passada para vendedora",
  "Agendamento em aberto",
  "Agendou",
  "Compareceu",
  "Comprou",
  "Não comprou",
  "Follow-up",
  "Perdida",
] as const;

export type PipelineStatus = (typeof PIPELINE_STATUSES)[number];

const API_BASE_URL = process.env.HARMONIZA_CRM_API_URL ?? "http://127.0.0.1:8000";
const API_TOKEN = process.env.HARMONIZA_CRM_API_TOKEN;

export async function fetchLeads(filters: LeadsFilters = {}): Promise<LeadsResult> {
  const params = new URLSearchParams();
  if (filters.status_atual) params.set("status_atual", filters.status_atual);
  if (filters.campanha) params.set("campanha", filters.campanha);
  params.set("limit", String(filters.limit ?? 50));

  try {
    const response = await fetch(`${API_BASE_URL}/leads?${params.toString()}`, {
      headers: API_TOKEN ? { Authorization: `Bearer ${API_TOKEN}` } : undefined,
      cache: "no-store",
    });

    if (!response.ok) {
      return { leads: [], unavailable: true };
    }

    return { leads: (await response.json()) as Lead[], unavailable: false };
  } catch {
    return { leads: [], unavailable: true };
  }
}

export async function updateLeadStage(
  leadId: number,
  payload: { novo_status: string; observacao?: string },
): Promise<boolean> {
  if (!API_TOKEN) return false;

  try {
    const response = await fetch(`${API_BASE_URL}/leads/${leadId}/stage`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${API_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      cache: "no-store",
    });

    return response.ok;
  } catch {
    return false;
  }
}
